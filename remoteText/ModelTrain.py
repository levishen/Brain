from Text_train import Train
PATH = 'xuangubao/offenceandviolationV3.xlsx'

def train():
    Text = Train(PATH)
    label, content, title,label_count = Text.read_execl()
    content_new = Text.clean_data(content)
    seg_content = Text.token(content_new)
    stop_content = Text.del_stop(seg_content)
    tf_tra = Text.cal_tf_idf(stop_content)
    X_train, X_test, y_train, y_test = Text.get_data(tf_tra,label)
    lr,y_pred = Text.get_model(X_train,y_train,X_test)
    score = Text.eva_model(True,y_test,y_pred)
    return score


if __name__ == '__main__':
    print(train())

