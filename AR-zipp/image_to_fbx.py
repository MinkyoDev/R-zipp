import os
import requests

from lib.preprocessing import PreProcessing
from lib.blend_to_fbx import BlendToFBX
from lib.data_condtrol_ import CreateDataset
from lib.generate_blueprint import BlueprintGenerator


preprocessing = PreProcessing()
converter = BlendToFBX()
create_dataset = CreateDataset()

model_path = "./models/G_no_ocr_binary_size1024_1109.pt"
generator = BlueprintGenerator(model_path)


class ImageToFBX():
    def __init__(self) -> None:
        pass

    def image_to_fbx_old(self, file_path):
        # Preprocessing
        ouput_path = 'statics/Images/After_preprocessing'
        preprocessing.run(file_path)
        preprocessing_result = preprocessing.file_save(ouput_path)

        # Image to blend file
        url = 'http://127.0.0.1:8001/blueprint_to_3D'

        data = {'ImagePath': preprocessing_result}

        response = requests.post(url, json=data)
        print(f'Status Code: {response.status_code}  /  Response Content : {response.text}')

        if response.status_code == 200:
            # Blend to fbx converter
            blend_name = response.text.replace('"','')
            blend_path = f"statics/blend_file/{blend_name}"

            fbx_dir = 'statics/fbx_file'
            fbx_file = converter.blend_to_fbx(blend_path, fbx_dir)

            print('convert successfully!')
            return fbx_file
        else:
            print(f'make bled error : {preprocessing_result}')
    
    
    def handimg_to_fbx(self, origin_image):
        # Image generating
        generator.data_load(image=origin_image)
        generator.parameter_setting(
                                want_img='all', 
                                add_origin=False, 
                                output_dir='./statics/generate_reault')
        generating_result, result_img = generator.run(save=True)
        
        # Image to blend file
        url = 'http://127.0.0.1:8001/blueprint_to_3D'

        data = {'ImagePath': generating_result}

        response = requests.post(url, json=data)
        print(f'Status Code: {response.status_code}  /  Response Content : {response.text}')

        # Blend to fbx converter
        if response.status_code == 200:
            blend_name = response.text.replace('"','')
            blend_path = f"statics/blend_file/{blend_name}"

            fbx_dir = 'statics/fbx_file'
            fbx_file_path = converter.blend_to_fbx(blend_path, fbx_dir, size_multiplier=2, desired_height=2.5)

            print('convert successfully!')
            return fbx_file_path.replace('\\', '/')
        else:
            print(f'make bled error : {generating_result}')


    def blueprint_to_fbx(self, origin_image):
        # Preprocessing
        create_dataset.data_load(image=origin_image)
        create_dataset.parameter_setting(
                                        limit=130, 
                                        aspect_ratio=1/1, 
                                        output_dir='./statics/uploads',
                                        new_width=800,
                                        padding_percent=0.1)
        preprocessing_result, result_img = create_dataset.run(save=True)
        
        # Image to blend file
        url = 'http://127.0.0.1:8001/blueprint_to_3D'

        data = {'ImagePath': preprocessing_result}

        response = requests.post(url, json=data)
        print(f'Status Code: {response.status_code}  /  Response Content : {response.text}')

        # Blend to fbx converter
        if response.status_code == 200:
            blend_name = response.text.replace('"','')
            blend_path = f"statics/blend_file/{blend_name}"

            fbx_dir = 'statics/fbx_file'
            fbx_file_path = converter.blend_to_fbx(blend_path, fbx_dir, size_multiplier=2, desired_height=2.5)

            print('convert successfully!')
            return fbx_file_path.replace('\\', '/')
        else:
            print(f'make bled error : {preprocessing_result}')
            
    
    def run(self, img_type, image):
        # mode select
        if img_type == 'HANDIMG':
            fbx_file = self.handimg_to_fbx(image)
            
        elif img_type == 'FLOORPLAN':
            fbx_file = self.blueprint_to_fbx(image)
            
        return fbx_file



if __name__ == '__main__':
    ItoFBX = ImageToFBX()
    
    img_type = ["HANDIMG", "FLOORPLAN"]
    # ItoFBX.run(img_type[0], image)

    # file = 'statics/Images/Original/image_000.jpg'
    # directory = 'statics/Images/Original'
    # file_list = os.listdir(directory)
    # for file_name in file_list[:20]:
    #     fbx_file = ItoFBX.image_to_fbx(os.path.join(directory, file_name))
    #     print('')