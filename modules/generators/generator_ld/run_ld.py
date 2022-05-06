# import torch
# from dalle2_pytorch import Unet, Decoder, CLIP, VQGanVAE

# # trained clip from step 1

# clip = CLIP(
#     dim_text = 512,
#     dim_image = 512,
#     dim_latent = 512,
#     num_text_tokens = 49408,
#     text_enc_depth = 1,
#     text_seq_len = 256,
#     text_heads = 8,
#     visual_enc_depth = 1,
#     visual_image_size = 256,
#     visual_patch_size = 32,
#     visual_heads = 8
# )

# # 3 unets for the decoder (a la cascading DDPM)

# # first two unets are doing latent diffusion
# # vqgan-vae must be trained beforehand

# vae1 = VQGanVAE(
#     dim = 32,
#     image_size = 256,
#     layers = 3,
#     layer_mults = (1, 2, 4)
# )

# vae2 = VQGanVAE(
#     dim = 32,
#     image_size = 512,
#     layers = 3,
#     layer_mults = (1, 2, 4)
# )

# unet1 = Unet(
#     dim = 32,
#     image_embed_dim = 512,
#     cond_dim = 128,
#     channels = 3,
#     sparse_attn = True,
#     sparse_attn_window = 2,
#     dim_mults = (1, 2, 4, 8)
# )

# unet2 = Unet(
#     dim = 32,
#     image_embed_dim = 512,
#     channels = 3,
#     dim_mults = (1, 2, 4, 8, 16),
#     cond_on_image_embeds = True,
#     cond_on_text_encodings = False
# )

# unet3 = Unet(
#     dim = 32,
#     image_embed_dim = 512,
#     channels = 3,
#     dim_mults = (1, 2, 4, 8, 16),
#     cond_on_image_embeds = True,
#     cond_on_text_encodings = False,
#     attend_at_middle = False
# )

# # decoder, which contains the unet(s) and clip

# decoder = Decoder(
#     clip = clip,
#     vae = (vae1, vae2),                # latent diffusion for unet1 (vae1) and unet2 (vae2), but not for the last unet3
#     unet = (unet1, unet2, unet3),      # insert unets in order of low resolution to highest resolution (you can have as many stages as you want here)
#     image_sizes = (256, 512, 1024),    # resolutions, 256 for first unet, 512 for second, 1024 for third
#     timesteps = 100,
#     image_cond_drop_prob = 0.1,
#     text_cond_drop_prob = 0.5
# ).cuda()

# # mock images (get a lot of this)

# images = torch.randn(1, 3, 1024, 1024).cuda()

# # feed images into decoder, specifying which unet you want to train
# # each unet can be trained separately, which is one of the benefits of the cascading DDPM scheme

# with decoder.one_unet_in_gpu(1):
#     loss = decoder(images, unet_number = 1)
#     loss.backward()

# with decoder.one_unet_in_gpu(2):
#     loss = decoder(images, unet_number = 2)
#     loss.backward()

# with decoder.one_unet_in_gpu(3):
#     loss = decoder(images, unet_number = 3)
#     loss.backward()

# # do the above for many steps for both unets

# # then it will learn to generate images based on the CLIP image embeddings

# # chaining the unets from lowest resolution to highest resolution (thus cascading)

# mock_image_embed = torch.randn(1, 512).cuda()
# images = decoder.sample(mock_image_embed) # (1, 3, 1024, 1024)