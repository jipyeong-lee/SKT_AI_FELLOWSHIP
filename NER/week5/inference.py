import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

MODEL_NAME = 'monologg/koelectra-base-v3-discriminator'
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

unique_tags = {'B-LOC', 'B-PER', 'I-LOC', 'I-PER', 'O'}
tag2id = {'B-LOC': 0, 'B-PER': 1, 'O': 2, 'I-PER': 3, 'I-LOC': 4}
id2tag = {0: 'B-LOC', 1: 'B-PER', 2: 'O', 3: 'I-PER', 4: 'I-LOC'}

model = AutoModelForTokenClassification.from_pretrained('koelectra', num_labels=len(unique_tags))
model.to(device)

pad_token_id = tokenizer.pad_token_id
cls_token_id = tokenizer.cls_token_id
sep_token_id = tokenizer.sep_token_id
pad_token_label_id = tag2id['O']
cls_token_label_id = tag2id['O']
sep_token_label_id = tag2id['O']

def ner_tokenizer(sent, max_seq_length):
    pre_syllable = "_"
    input_ids = [pad_token_id] * (max_seq_length - 1)
    attention_mask = [0] * (max_seq_length - 1)
    token_type_ids = [0] * max_seq_length
    sent = sent[:max_seq_length - 2]

    for i, syllable in enumerate(sent):
        if syllable == '_':
            pre_syllable = syllable
        if pre_syllable != "_":
            syllable = '##' + syllable
        pre_syllable = syllable

        input_ids[i] = (tokenizer.convert_tokens_to_ids(syllable))
        attention_mask[i] = 1

    input_ids = [cls_token_id] + input_ids
    input_ids[len(sent) + 1] = sep_token_id
    attention_mask = [1] + attention_mask
    attention_mask[len(sent) + 1] = 1
    return {"input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids}


def ner_inference(text):
    model.eval()
    text = text.replace(' ', '_')

    predictions, true_labels = [], []

    tokenized_sent = ner_tokenizer(text, len(text) + 2)
    input_ids = torch.tensor(tokenized_sent['input_ids']).unsqueeze(0).to(device)
    attention_mask = torch.tensor(tokenized_sent['attention_mask']).unsqueeze(0).to(device)
    token_type_ids = torch.tensor(tokenized_sent['token_type_ids']).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids)

    logits = outputs['logits']
    logits = logits.detach().cpu().numpy()
    label_ids = token_type_ids.cpu().numpy()

    predictions.extend([list(p) for p in np.argmax(logits, axis=2)])
    true_labels.append(label_ids)

    pred_tags = [list(tag2id.keys())[p_i] for p in predictions for p_i in p]

    print('{}\t{}'.format("TOKEN", "TAG"))
    print("===========")
    # for token, tag in zip(tokenizer.decode(tokenized_sent['input_ids']), pred_tags):
    #   print("{:^5}\t{:^5}".format(token, tag))
    for i, tag in enumerate(pred_tags):
        print("{:^5}\t{:^5}".format(tokenizer.convert_ids_to_tokens(tokenized_sent['input_ids'][i]), tag))


if __name__ == '__main__':
    text = input('input : ')
    ner_inference(text)