import laspy
import numpy as np
import os
import pandas as pd
from functools import wraps


def batch2(input_suffix, output_suffix):
    """
    Used as decorator. Converting files in the input_folder from input_suffix to output_suffix format and saved in the output_folder
    :param input_suffix: the input format of files
    :param output_suffix: the output format of files
    :return: True: successed, False: failed
    """
    def batch_format_converter(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = True
            if len(args) != 2:
                ret = False
                print('Number of parameters should be 2, instead of {}'.format(args))
            else:

                input_folder = args[0]
                output_folder = args[1]

                filenames = os.listdir(input_folder)
                for filename in filenames:
                    if os.path.splitext(filename)[1] != input_suffix:
                        continue
                    input_path = os.path.join(input_folder, filename)
                    _filename = os.path.splitext(filename)[0] + output_suffix
                    output_path = os.path.join(output_folder, _filename)
                    func(input_path, output_path)
            return ret
        return wrapper
    return batch_format_converter


def csv2las(csv_path, las_path):
    """
    Converting csv file to las file
    :param csv_path: string, path to the input csv file
    :param las_path: string, path to save the las file
    :return:
    """
    mat = csv2numpy(csv_path)
    numpy2las(mat, las_path)


def csv2numpy(csv_path):
    """
    Converting csv file to ndarray
    :param csv_path: string, path to read the csv file
    :return: ndarray
    """
    data_ori = pd.read_csv(csv_path)
    data_matrix = np.array(data_ori)
    return data_matrix


def numpy2csv(mat, csv_path):
    """
    Converting ndarray to csv file
    :param mat: ndarray
    :param csv_path: string, path to save csv file
    :return:
    """
    np.savetxt(csv_path, mat, fmt='%f', delimiter=',')

def txt2numpy(txt_path):
    """
    Load txt data and convert to ndarray
    :param txt_path: string, path to txt file
    :return: ndarray
    """
    mat = np.loadtxt(txt_path)
    return mat

def numpy2las(mat, las_path='demo.las'):
    """
    Saving the ndarray points data into a .las file.
    :param mat: ndarray
    :param las_path: string, path to save the las file
    :return:
    """
    #mat = mat[mat[:, 1] < 40]
    myheader = laspy.header.Header()
    outfile = laspy.file.File(las_path, mode="w", header=myheader)
    outfile.header.scale = [0.001, 0.001, 0.001, 0.001]

    outfile.x = mat[:, 0]
    outfile.y = mat[:, 1]
    outfile.z = mat[:, 2]

    if mat.shape[1] == 3:
        outfile.intensity = np.ones_like(mat[:, 0])
    else:
        outfile.intensity = mat[:, 3]
        #outfile.intensity = np.ones_like(mat[:, 0])

    outfile.close()


@batch2(input_suffix='.csv', output_suffix='.las')
def batch_csv2las(csv_path, las_path):
    """
    Converting csv file in a folder to las file. Call this function as batch_csv2las(input_folder, output_folder)
    :param csv_path: string, path to the input csv file
    :param las_path: string, path to save the las file
    :return:
    """
    mat = csv2numpy(csv_path)
    numpy2las(mat, las_path)


def csv2las_grid(csv_path, las_path, grid_xy=0.05):
    mat = csv2numpy(csv_path)
    mat[:, 0:2] *= grid_xy
    numpy2las(mat, las_path)


def ini2las_grid(ini_path_1, ini_path_2, las_path, grid_xy=0.2):
    mat1 = txt2numpy(ini_path_1)
    mat2 = txt2numpy(ini_path_2)
    mat = np.concatenate((mat1, mat2))
    mat[:, 0:2] *= grid_xy
    mat[:, 3] = 1
    mask = mat[:, 0] > -2
    mat = mat[mask]
    mask2 = mat[:, 0] < 32
    mat = mat[mask2]
    numpy2las(mat, las_path)


if __name__ == '__main__':
    #csv2las("C:\\home\\temp\\33897\\build\\bin\\Release\\csvData\\voxelBackground.csv",
    #        "C:\\home\\temp\\33897\\build\\bin\\Release\\csvData\\voxelBackground.las")
    #csv2las("C:\\home\\temp\\33897\\build\\bin\\Release\\csvData\\pointsBuffer.csv",
    #        "C:\\home\\temp\\33897\\build\\bin\\Release\\csvData\\pointsBuffer.las")
    csv2las_grid("C:\\home\\temp\\33897\\build\\bin\\Release\\csvData\\surface.csv",
                 "C:\\home\\temp\\33897\\build\\bin\\Release\\csvData\\surface.las")
    #ini2las_grid("C:\\home\\temp\\33897\\build\\bin\\Release\\g_0_oground.ini",
    #             "C:\\home\\temp\\33897\\build\\bin\\Release\\g_1_oground.ini",
    #             "C:\\home\\temp\\33897\\build\\bin\\Release\\csvData\\ground.las")






