import pandas as pd
def who_am_i():
    print("Hello my name is Clement")
if __name__ == '__main__':
    who_am_i()

def simple_df():
    df = pd.DataFrame([['Alice', 25], ['Bob', 30]], columns=['Name', 'Age'])
    return df

simple_df()