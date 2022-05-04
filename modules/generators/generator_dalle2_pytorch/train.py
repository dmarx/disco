import json
import os
from types import SimpleNamespace
import PIL
from dalle2_pytorch.cli import get_pkg_version, safeget, simple_slugify
from dalle2_pytorch.dalle2_pytorch import (
    DALLE2,
    Decoder,
    DiffusionPrior,
    DiffusionPriorNetwork,
    OpenAIClipAdapter,
    Unet,
)
import torch
from pathlib import Path
import torchvision.transforms as T
from functools import reduce, partial
import click


def main():
    print("Training...")
    do_run_openai("An apple")


def do_run_openai(prompt):

    clip = OpenAIClipAdapter()

    # mock data

    text = torch.randint(0, 49408, (4, 256)).cuda()
    images = torch.randn(4, 3, 256, 256).cuda()

    # prior networks (with transformer)

    prior_network = DiffusionPriorNetwork(dim=512, depth=6, dim_head=64, heads=8).cuda()

    diffusion_prior = DiffusionPrior(
        net=prior_network, clip=clip, timesteps=100, cond_drop_prob=0.2
    ).cuda()

    loss = diffusion_prior(text, images)
    loss.backward()

    # do above for many steps ...

    # decoder (with unet)

    unet1 = Unet(
        dim=128, image_embed_dim=512, cond_dim=128, channels=3, dim_mults=(1, 2, 4, 8)
    ).cuda()

    unet2 = Unet(
        dim=16,
        image_embed_dim=512,
        cond_dim=128,
        channels=3,
        dim_mults=(1, 2, 4, 8, 16),
    ).cuda()

    decoder = Decoder(
        unet=(unet1, unet2),
        image_sizes=(128, 256),
        clip=clip,
        timesteps=100,
        image_cond_drop_prob=0.1,
        text_cond_drop_prob=0.5,
        # set this to True if you wish to condition on text during training and sampling
        condition_on_text_encodings=False,
    ).cuda()

    for unet_number in (1, 2):
        # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
        loss = decoder(images, unet_number=unet_number)
        loss.backward()

    # do above for many steps

    dalle2 = DALLE2(prior=diffusion_prior, decoder=decoder)

    images = dalle2(
        [prompt],
        # classifier free guidance strength (> 1 would strengthen the condition)
        cond_scale=2.0,
    )

    filename_gen = f"dalle_out.png"
    for img in images:
        try:
            pil_image = T.ToPILImage()(img)
            pil_image.save("content/output/" + filename_gen)
        except Exception as inst:
            print(inst)  # __str__ allows args to be printed directly,

    return filename_gen


if __name__ == "__main__":
    main()
