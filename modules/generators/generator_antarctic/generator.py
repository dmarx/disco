from modules.generators.base.generator import GeneratorBase

import argparse
import io
import numpy as np
import torch
import torch.nn as nn
import requests
import pytorch_lightning as pl
import matplotlib.pyplot as plt
import torchvision.transforms.functional as F

from CLIP import clip
from PIL import Image
from pytorch_lightning.callbacks import ModelCheckpoint
from torchvision.utils import make_grid


class GeneratorArbitrary(GeneratorBase):
    """This generator will caption an image using Antarctic captions."""

    settings = {
        "prompt": "",
        "code": "",
        "init_image": "",
        "i_generator": 0,
        "device": "cuda:0",
        "clip_model": "ViT-B/16",
    }

    def do_run(self, prefix="", input_seed=""):
        def wget(url, outputdir, filename=None):
            if filename is not None:
                res = subprocess.run(
                    ["wget", url, "-O", f"{os.path.join(outputdir, filename)}"],
                    stdout=subprocess.PIPE,
                ).stdout.decode("utf-8")
            else:
                res = subprocess.run(
                    ["wget", url, "-P", f"{outputdir}"], stdout=subprocess.PIPE
                ).stdout.decode("utf-8")
            print(res)

        def createPath(filepath):
            os.makedirs(filepath, exist_ok=True)

        PROJECT_DIR = os.getcwd()

        def download_model(filename, url, PROJECT_DIR=PROJECT_DIR, md5=None):
            filepath = f"{PROJECT_DIR}/content/models/pretrained/{filename}"
            if os.path.exists(filepath):
                return
                # md5 is different each time file is downloaded, don't use for now
                # if md5 is not None:
                #     if get_digest(filepath) == md5:
                #         print('matching md5')
                #         return
            createPath(f"{PROJECT_DIR}/content/models/pretrained")
            wget(url, f"{PROJECT_DIR}/content/models/pretrained", filename=filename)
            # print('md5 hash:', get_digest(filepath), md5)

        download_model(
            "-epoch=05-vloss=2.163.ckpt",
            "https://the-eye.eu/public/AI/models/antarctic-captions/-epoch=05-vloss=2.163.ckpt",
        )
        download_model(
            "postcache.txt",
            "https://the-eye.eu/public/AI/models/antarctic-captions/postcache.txt",
        )
        download_model(
            "postcache.npy",
            "https://the-eye.eu/public/AI/models/antarctic-captions/postcache.npy",
        )

        def gitclone(url, path=None):
            if path is None:
                res = subprocess.run(
                    ["git", "clone", url], stdout=subprocess.PIPE
                ).stdout.decode("utf-8")
            else:
                if not os.path.exists(path):
                    os.makedirs(path)
                res = subprocess.run(
                    ["git", "-C", path, "clone", url], stdout=subprocess.PIPE
                ).stdout.decode("utf-8")
            print(res)

        gitclone(
            "https://github.com/dzryk/antarctic-captions.git",
            path="lib/antarctic_captions",
        )

        import lib.antarctic_captions.model, lib.antarctic_captions.utils

        device = torch.device(
            settings["device"] if torch.cuda.is_available() else "cpu"
        )
        print("Using device:", device)

        # Helper functions
        def fetch(url_or_path):
            if str(url_or_path).startswith("http://") or str(url_or_path).startswith(
                "https://"
            ):
                r = requests.get(url_or_path)
                r.raise_for_status()
                fd = io.BytesIO()
                fd.write(r.content)
                fd.seek(0)
                return fd
            return open(url_or_path, "rb")

        def load_image(img, preprocess):
            img = Image.open(fetch(img))
            return img, preprocess(img).unsqueeze(0).to(device)

        def show(imgs):
            if not isinstance(imgs, list):
                imgs = [imgs]
            fix, axs = plt.subplots(ncols=len(imgs), squeeze=False)
            for i, img in enumerate(imgs):
                img = img.detach()
                img = F.to_pil_image(img)
                axs[0, i].imshow(np.asarray(img))
                axs[0, i].set(xticklabels=[], yticklabels=[], xticks=[], yticks=[])

        def display_grid(imgs):
            reshaped = [F.to_tensor(x.resize((256, 256))) for x in imgs]
            show(make_grid(reshaped))

        def clip_rescoring(args, net, candidates, x):
            textemb = net.perceiver.encode_text(
                clip.tokenize(candidates).to(args.device)
            ).float()
            textemb /= textemb.norm(dim=-1, keepdim=True)
            similarity = (100.0 * x @ textemb.T).softmax(dim=-1)
            _, indices = similarity[0].topk(args.num_return_sequences)
            return [candidates[idx] for idx in indices[0]]

        def loader(args):
            cache = []
            with open(args.textfile) as f:
                for line in f:
                    cache.append(line.strip())
            cache_emb = np.load(args.embfile)
            net = utils.load_ckpt(args)
            net.cache = cache
            net.cache_emb = torch.tensor(cache_emb).to(args.device)
            preprocess = clip.load(args.clip_model, jit=False)[1]
            return net, preprocess

        def caption_image(path, args, net, preprocess):
            captions = []
            img, mat = load_image(path, preprocess)
            table, x = utils.build_table(
                mat.to(device),
                perceiver=net.perceiver,
                cache=net.cache,
                cache_emb=net.cache_emb,
                topk=args.topk,
                return_images=True,
            )
            table = net.tokenizer.encode(table[0], return_tensors="pt").to(device)
            out = net.model.generate(
                table,
                do_sample=args.do_sample,
                num_beams=args.num_beams,
                temperature=args.temperature,
                top_p=args.top_p,
                num_return_sequences=args.num_return_sequences,
            )
            candidates = []
            for seq in out:
                candidates.append(net.tokenizer.decode(seq, skip_special_tokens=True))
            captions = clip_rescoring(args, net, candidates, x[None, :])
            for c in captions[: args.display]:
                print(c)
            display_grid([img])
            return captions

        # Settings
        modeldir = f"{PROJECT_DIR}/content/models/pretrained"
        args = argparse.Namespace(
            ckpt=f"{modeldir}/-epoch=05-vloss=2.163.ckpt",
            textfile=f"{modeldir}/postcache.txt",
            embfile=f"{modeldir}/postcache.npy",
            clip_model=self.settings["clip_model"],
            topk=10,
            num_return_sequences=1000,
            num_beams=1,
            temperature=1.0,
            top_p=1.0,
            display=5,
            do_sample=True,
            device=device,
        )

        # Load checkpoint and preprocessor
        net, preprocess = loader(args)

        captions = caption_image(self.settings["init_image"], args, net, preprocess)
        print(captions)
        # XXX: Figure out data structure for returns
        return captions

    def init_settings(self, override_settings=None):

        settings = self.settings

        if override_settings != None:
            settings = self.json_override(settings, override_settings)

    def __init__(self, chain):
        super().__init__(chain)
        self.title = "Antarctic Captioning"
