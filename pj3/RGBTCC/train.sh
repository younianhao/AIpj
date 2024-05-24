python train.py \
    --data-dir ./rgbtcc_dataset/ \
    --save-dir ./model \
    --pretrained_model ../model/model_best.pth.tar\
    --batch-size 8 \
    --lr 1e-5 \
    --device 0