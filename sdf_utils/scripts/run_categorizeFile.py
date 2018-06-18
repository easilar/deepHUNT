###%run sdf_utils/scripts/categorizeFile.py --inputpath='sdf_utils/data/imbalanced_learning_datasets/testSet/Cholestasis_human_test/sdf/Cholestasis_human_test_231cpds_moeDesc.sdf' --outpath='sdf_utils/data/categorized_imbalanced_human/test/' --keys='class'

%run sdf_utils/scripts/categorizeFile.py --inputpath='sdf_utils/data/muliner/Mulliner_H_MF_HB_1_conf.sdf' --outpath='sdf_utils/data/muliner/categorised_H_MF_HB_1/' --keys='ID Class Fold'


%run sdf_utils/scripts/categorizeFile.py --inputpath='sdf_utils/data/imbalanced_learning_datasets/trainingSet/cholestasis_
human/sdf/Cholestasis_human_1766_moeDesc.sdf' --outpath='sdf_utils/data/categorized_imbalanced_human/training/' --keys='ID class'

