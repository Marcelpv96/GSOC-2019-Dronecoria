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
To modify the train data, you have to first: Create your own dataset, then modify some files on the project to make the system able to work with another data.
#### Create your own Data Set
