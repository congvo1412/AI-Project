from torchvision import transforms
import base64
from io import BytesIO
from .dressing_in_order.datasets_ import DFVisualDataset


transform = transforms.ToPILImage()


def load_img(pid):
    person = inputs[pid[0]]

    # person = (i.cuda() for i in person)
    pimg, parse, to_pose = person
    pimg, parse, to_pose = pimg[pid[1]], parse[pid[1]], to_pose[pid[1]]

    return pimg.squeeze(), parse.squeeze(), to_pose.squeeze()


def convert_to_pil(tensor):
    pil_img = transform(tensor)
    
    return pil_img
    

def convert_to_base64(tensor):
    tensor = (tensor + 1) / 2
    pil_img = transform(tensor)

    buffered = BytesIO()
    pil_img.save(buffered, format="JPEG")

    base64_img = base64.b64encode(buffered.getvalue()).decode("utf-8")
    result = f"data:image/jpeg;base64,{base64_img}"

    return pil_img, result


dataroot = "backend/dressing_in_order/data/"

Dataset = DFVisualDataset
ds = Dataset(dataroot=dataroot, dim=(256, 176), n_human_part=8)

inputs = dict()
for attr in ds.attr_keys:
    inputs[attr] = ds.get_attr_visual_input(attr)


meta = []
images = []
pil_images = []


for key in inputs:
    for i in range(len(inputs[key][0])):
        pid = (key, i, None)
        pimg, _, _ = load_img(pid)
        meta.append(f"{key}_{i}")
        pil_image, base64_image = convert_to_base64(pimg)
        images.append(base64_image)
        pil_images.append(pil_image)
        
        
img_index = meta.index("print_2")

meta_ = meta[img_index]
img = images[img_index]
pil_img = pil_images[img_index]

images.insert(1, img)
pil_images.insert(1, pil_img)
meta.insert(1, meta_)


img_index = meta.index("plaid_3")
meta_ = meta[img_index]
img = images[img_index]
pil_img = pil_images[img_index]

images.insert(1, img)
pil_images.insert(1, pil_img)
meta.insert(1, meta_)

