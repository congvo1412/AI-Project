import numpy as np


from .dressing_in_order.models.dior_model import DIORModel
from .dataset import load_img

dataroot = "backend/dressing_in_order/data"
exp_name = "DIORv1_64"  # DIOR_64
epoch = "latest"
netG = "diorv1"  # dior
ngf = 64


class Opt:
    def __init__(self):
        pass


if True:
    opt = Opt()
    opt.dataroot = dataroot
    opt.isTrain = False
    opt.phase = "test"
    opt.n_human_parts = 8
    opt.n_kpts = 18
    opt.style_nc = 64
    opt.n_style_blocks = 4
    opt.netG = netG
    opt.netE = "adgan"
    opt.ngf = ngf
    opt.norm_type = "instance"
    opt.relu_type = "leakyrelu"
    opt.init_type = "orthogonal"
    opt.init_gain = 0.02
    opt.gpu_ids = [0]
    opt.frozen_flownet = True
    opt.random_rate = 1
    opt.perturb = False
    opt.warmup = False
    opt.name = exp_name
    opt.vgg_path = ""
    opt.flownet_path = ""
    opt.checkpoints_dir = "backend/dressing_in_order/checkpoints"
    opt.frozen_enc = True
    opt.load_iter = 0
    opt.epoch = epoch
    opt.verbose = False
    opt.gpu_ids = None


def combine_result(pimg=[], gimgs=[], oimgs=[], gen_img=[], pose=None):
    out = gen_img
    out = out.float().cpu().detach().numpy()
    out = (out + 1) / 2  # denormalize
    out = np.transpose(out, [1, 2, 0])

    out = out * 255
    out = out.astype(np.uint8)
    return out


def _dress_in_order(
    model, pid, pose_id=None, gids=[], ogids=[], order=[5, 1, 3, 2],
    perturb=False
):
    PID = [0, 4, 6, 7]
    # encode person
    pimg, parse, from_pose = load_img(pid)
    if not pose_id:
        to_pose = from_pose
    else:
        to_img, _, to_pose = load_img(pose_id)
    psegs = model.encode_attr(
        pimg[None], parse[None], from_pose[None], to_pose[None], PID
    )

    # encode base garments
    gsegs = model.encode_attr(
        pimg[None], parse[None], from_pose[None], to_pose[None]
    )

    # swap base garment if any
    gimgs = []
    for gid in gids:
        _, _, k = gid
        gimg, gparse, pose = load_img(gid)
        seg = model.encode_single_attr(
            gimg[None], gparse[None], pose[None], to_pose[None], i=gid[2]
        )
        gsegs[gid[2]] = seg
        gimgs += [gimg * (gparse == gid[2])]

    # encode garment (overlay)
    over_gsegs = []
    oimgs = []
    for gid in ogids:
        oimg, oparse, pose = load_img(gid)
        oimgs += [oimg * (oparse == gid[2])]
        seg = model.encode_single_attr(
            oimg[None], oparse[None], pose[None], to_pose[None], i=gid[2]
        )
        over_gsegs += [seg]

    gsegs = [gsegs[i] for i in order] + over_gsegs
    gen_img = model.netG(to_pose[None], psegs, gsegs)

    return pimg, gimgs, oimgs, gen_img[0], to_pose


model = DIORModel(opt)
model.setup(opt)
