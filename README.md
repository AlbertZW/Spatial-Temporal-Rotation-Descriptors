# Advanced Skeleton-Based Action Recognition via Spatial-Temporal Rotation Descriptors
## Overview
![](./Rotation_descriptors.png)
**Figure (a)** shows the movement of the joint unit constructed on the shoulder at adjacent sample moments. In **Figure (b)**, angles of bias *θ* and *φ* denote the rotation axis *n*. The linear combination of angles *(θ, φ, ψ)* constructs **Rotation Angles Representation (RAR)**. In **Figure (c)**, *α<sub>1</sub>, α<sub>2</sub>* are the internal angles between two bones *e<sub>m</sub>* and *e<sub>n</sub>* on the tangential direction and *β* is the angular difference between norm vectors *p*. The angular differences on the tangential and normal directions *α<sub>2</sub> − α<sub>1</sub>* and *β* construct **Two-Directional Difference Representation (2DDR)**.

## Usage
Rotation descriptors are complementary input features for skeleton-based action recognition and can be applied in any algorithms. We take [2S-AGCN](https://github.com/lshiwjx/2S-AGCN) as example:

We first merge the files in ```./data_gen``` of our repository with the one in 2S-AGCN, generate rotation features of NTU dataset with:
```
python data_gen/ntu_gen-preprocess.py
```
The configuration of our current code is for RAR. The related codes start with the comment ```# added for generate Rotation Descriptors```. Note that since the dimension of RAR for each joint unit is 3 while 2DDR is 2, do not forget the change the code in **line 122** to reconfigure.

The configurations of the neural network should also be modified according to the proposed rotation descriptors.  Files in ```./config``` and ```./graph``` are the configurations for 2S-AGCN.

We also provide the matlab code for generating rotation features in FPHA, the usage is similar. 

## Citation
```
@article{shen2021advanced,
  title={Advanced skeleton-based action recognition via spatial--temporal rotation descriptors},
  author={Shen, Zhongwei and Wu, Xiao-Jun and Kittler, Josef},
  journal={Pattern Analysis and Applications},
  pages={1--12},
  year={2021},
  publisher={Springer}
}
```
