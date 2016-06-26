from SequenceGenerator import *
import shutil

if __name__ == '__main__':
   treelist = ["edge01CDE","edge02CDE","edge04CDE","edge06CDE","edge08CDE","edge10CDE",
                "leaf01sameedges","leaf02sameedges","leaf04sameedges","leaf06sameedges","leaf08sameedges","leaf10sameedges"]

 
    seq_exe_dir = "c:\\seqgen\\"

    

    # Run Seq-Gen  with default GTR parameters
    for t in treelist:
        tree = t 
        for i in range(0,100):
            if not os.path.exists(seq_exe_dir + tree + "\\" + tree + str(i) + ".nex"):
                tree_gen = SequenceGenerator(tree + str(i),"c:\\seqgen\\" + tree + ".txt",evomodel = "GTR")
                tree_gen.runseq_gen()
            shutil.copyfile(seq_exe_dir + tree + str(i) + ".txt", seq_exe_dir + "\\" + tree + str(i) + "\\" + tree + str(i) + ".txt")