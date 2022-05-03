# import torch
# from dalle2_pytorch import DALLE2, DiffusionPriorNetwork, DiffusionPrior, Unet, Decoder, OpenAIClipAdapter

# # openai pretrained clip - defaults to ViT/B-32

# clip = OpenAIClipAdapter()

# # mock data

# text = torch.randint(0, 49408, (4, 256)).cuda()
# images = torch.randn(4, 3, 256, 256).cuda()

# # prior networks (with transformer)

# prior_network = DiffusionPriorNetwork(
#     dim=512,
#     depth=6,
#     dim_head=64,
#     heads=8
# ).cuda()

# diffusion_prior = DiffusionPrior(
#     net=prior_network,
#     clip=clip,
#     timesteps=100,
#     cond_drop_prob=0.2
# ).cuda()

# loss = diffusion_prior(text, images)
# loss.backward()

# # do above for many steps ...

# # decoder (with unet)

# unet1 = Unet(
#     dim=128,
#     image_embed_dim=512,
#     cond_dim=128,
#     channels=3,
#     dim_mults=(1, 2, 4, 8)
# ).cuda()

# unet2 = Unet(
#     dim=16,
#     image_embed_dim=512,
#     cond_dim=128,
#     channels=3,
#     dim_mults=(1, 2, 4, 8, 16)
# ).cuda()

# decoder = Decoder(
#     unet=(unet1, unet2),
#     image_sizes=(128, 256),
#     clip=clip,
#     timesteps=100,
#     image_cond_drop_prob=0.1,
#     text_cond_drop_prob=0.5,
#     # set this to True if you wish to condition on text during training and sampling
#     condition_on_text_encodings=False
# ).cuda()

# for unet_number in (1, 2):
#     # this can optionally be decoder(images, text) if you wish to condition on the text encodings as well, though it was hinted in the paper it didn't do much
#     loss = decoder(images, unet_number=unet_number)
#     loss.backward()

# # do above for many steps

# dalle2 = DALLE2(
#     prior=diffusion_prior,
#     decoder=decoder
# )

# images = dalle2(
#     ['a butterfly trying to escape a tornado'],
#     # classifier free guidance strength (> 1 would strengthen the condition)
#     cond_scale=2.
# )

# # save your image (in this example, of size 256x256)
