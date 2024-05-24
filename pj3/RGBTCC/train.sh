python train.py \
    --data-dir ./rgbtcc_dataset/ \
    --save-dir ./model \
    --pretrained_model ./pretrained/best_model.pth \
    --max-epoch 150 \
    --batch-size 8 \
    --lr 1e-5 \
    --device 0