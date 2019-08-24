# Google Summer Of Code,  2019 Dronecoria Project

This project is the result of the work done during the three months of Google Of Summer of Code internship. This project is a web Application that works with Liquid Galaxy as the visualization tool, and brings to the user the power to send images of burnt regions, and detect them using a Machine Learning model, previously trained by the user.

Files too big, to be on the _GitHub_ repository.

- Dataset folder: https://drive.google.com/drive/folders/11ukhnvOV44gJAdELYuSF8k81Mzg5rFaf (The user can change it, and train the model to detect another kind of burnt regions)


- DB with the data for the demonstrations: https://drive.google.com/file/d/17CWfFS8j2SaKJsVfoktqman_-pvwHtfY/view?usp=sharing


## 1  Installation

For this project is necessary a Python3.7 >= Version.

Git clone and download Dataset folder and DB folder.
> git clone https://github.com/Marcelpv96/GSOC-2019-Dronecoria.git

After done that, you have to have the folders structured like this tre:
```
GSOC 2019 Dronecoria Project
│   README.md
│
└─── Model
│   │   Dataset
│   │   Research
│   │   ...
│   
└─── Dronecoria
    │   db.sqlite3
    │   ...
....
```

Then you have to install requirements from 'requirements.txt'  file
> pip install -r 'requirements.txt'

Configure your LG API IP
> cd ~/
> export API_IP=your api ip

Finally
> cd Dronecoria
> python manage.py runserver yourip:port


Doing that, the software will works correctly, and all the content of the demonstration will be inside it, to test and visualize them. If you have encountered some issue during the process, feel free to open a issue. If you have some improvement in the system, feel free to make a pull requests. :)

## 2  Machine Learning Model
This project use DeepLab as the tool to do the semantic image segmentation. To learn clearly how it works, I encorage you to learn about it int he main repository here: [DeepLab](https://github.com/tensorflow/models/tree/master/research/deeplab). This point will be only a brief explaination of how to train the model with other data. This project now is configured to work as a prototype with synthetic data.


### 2.1 Modify train data
This will be a modification and adaptation of the instructions that appears on [this post](http://hellodfan.com/2018/07/06/DeepLabv3-with-own-dataset/). So, to modify the train data, you have to first: Create your own dataset, then modify some files on the project to make the system able to work with another data.
#### Create your own Data Set

You have to create your Dataset, and label it. The way to do that is simple, if for example you have only two classes, BackGround, Ignore pixels, burnt region pixels. Generates a single channel image, (image in grayscale) and all the pixels will have value 0 (this will be the background), then all the pixels that corresponds to the burnt region will have value 1. In the case that you have N classes to detect, the pixels that correspond to first class will be 1, second class 2, and so on and so for.


#### Index creation

You have to modify the content of the files inside : /GSOC-2019-Dronecoria/model/dataset/list_folder
- train.txt	: Name of files that will correspond to training set. ONLY THE NAME, not the path nor the extension.
- trainval.txt: Name of files that will correspond to cross validation set. ONLY THE NAME, not the path nor the extension.
- val.tx: Nome of files that wil correspond to test set. ONLY THE NAME, not the path nor the extension.

#### TFRecord data Generation

On the root of the project, appears a file named commands. Inside this file there are the commands to create TFRecord, train and validate your model. But here appears another time.

> cd GSOC-2019-Dronecoria/model/research/deeplab/datasets


>python build_voc2012_data.py \
>       --image_folder="${IMAGE_FOLDER}" \
>       --semantic_segmentation_folder="${SEMANTIC_SEG_FOLDER}" \
>       --list_folder="${LIST_FOLDER}" \
>       --image_format="jpg" \
>       --output_dir="${OUTPUT_DIR}"


- ${IMAGE_FOLDER} : the path of saving original images
- ${SEMANTIC_SEG_FOLDER}: the path of saving masks
- ${LIST_FOLDER}: the path of three index files
- image_format: the format of original images, and it is png format in my case
- output_dir: the path for saving generated TFRecord files (mkdir by yourself)

### 2.2 Train

#### Modify training script

First file to modify: GSOC-2019-Dronecoria/model/research/deeplab/datasets/data_generator.py
- In line 100 appears :
```python
_BURNTFOREST_INFORMATION = DatasetDescriptor(
    splits_to_sizes={
        'train': 161,  # num of samples in images/training
        'val': 45,  # num of samples in images/validation
    },
    num_classes=3,
    ignore_label=255,
)
```
- _BURNTFOREST_INFORMATION: Name of your dataset
- 'train': Number of training samples
- 'val': Number of val samples
- num_classes: number of classes (background, ignore, burnt) at least we will have 3 classes always.
- ignore_label: code for the ignore pixels


Then in line 109:
```python
_DATASETS_INFORMATION = {
    'cityscapes': _CITYSCAPES_INFORMATION,
    'pascal_voc_seg': _PASCAL_VOC_SEG_INFORMATION,
    'ade20k': _ADE20K_INFORMATION,
    'mydata': _BURNTFOREST_INFORMATION, # burnt dataset
}
```
- 'mydata' : name of my dataset


#### Training
Only pick one command


> python3 deeplab/train.py \
>       --logtostderr \
>       --training_number_of_steps=900 \
>       --train_split="train" \
>       --model_variant="xception_65" \
>       --atrous_rates=6 \
>       --atrous_rates=12 \
>       --atrous_rates=18 \
>       --output_stride=16 \
>       --decoder_output_stride=4 \
>       --train_crop_size=321,321 \
>       --train_batch_size=4 \
>        --dataset="mydata" \
>        --tf_initial_checkpoint='/Users/Marcelpv96/Dropbox/UNI/LiquidLGalaxy/GSOC-2019-Dronecoria/model/research/deeplab/backbone/deeplabv3_cityscapes_train/model.ckpt' \
>       --train_logdir='/Users/Marcelpv96/Dropbox/UNI/LiquidLGalaxy/GSOC-2019-Dronecoria/model/research/deeplab/burnt_forest/train' \
>   --dataset_dir='/Users/Marcelpv96/Dropbox/UNI/LiquidLGalaxy/GSOC-2019-Dronecoria/model/dataset/output'

- tf_initial_checkpoint: The path of pretrained weights. Because CamVid are similar to CityScapes, so we use pretrain weight on CityScapes
- train_logdir: The path of training checkpoint files
- dataset_dir: The path of dataset TFRecord files
- dataset: The name of dataset description in segmentation_dataset.py



### 2.3 Visualization

Validate that your model works:

> python deeplab/eval.py \
>       --logtostderr \
>       --vis_split="val" \
>       --model_variant="xception_65" \
>       --atrous_rates=6 \
>       --atrous_rates=12 \
>       --atrous_rates=18 \
>       --output_stride=16 \
>       --decoder_output_stride=4 \
>       --vis_crop_size=812,948 \
>       --dataset="mydata" \
>       --colormap_type="pascal" \
>       --checkpoint_dir='/Users/Marcelpv96/Dropbox/UNI/LiquidLGalaxy/GSOC-2019-Dronecoria/model/research/deeplab/burnt_forest/train' \
>       --vis_logdir='/Users/Marcelpv96/Dropbox/UNI/LiquidLGalaxy/GSOC-2019-Dronecoria/model/research/deeplab/burnt_forest/vis' \
>       --dataset_dir='/Users/Marcelpv96/Dropbox/UNI/LiquidLGalaxy/GSOC-2019-Dronecoria/model/dataset/output'


### 2.4 Freeze your model

Export your model, and put the path of your model inside the variable MODEL_PATH of GSOC-2019-Dronecoria/blob/master/dronecoria/dronecoria/settings.py

TO DO
