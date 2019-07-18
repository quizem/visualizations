import pandas as pd
def load_data(path='',sheetname=None):
    """ Load data 
    Params:
    ======
        path: str, path to file
        
    Output:
    =======
        pandas dataframe
    """
    if path.split('.')[-1]=='csv':
        df = pd.read_csv(path,sep=',')
    elif path.split('.')[-1]=='xlsx':
        df = pd.read_excel(path,sheet_name=sheetname)
    print('Number of records: ',df.shape[0])
    print('Number of columns: ',df.shape[1])
    return df

def preview_data(df, start=0, end=5):
    """Easily preview any slice of the data
    
    Params:
    =======
        start: int, start index 
        end: int, end index
        
    Output:
    =======
        data slice
    """
    return df.loc[start:end]

def check_duplicates(df,count_unique=True,subset=''):
    """Checks for duplicate records
    
    Params:
    =======
        df: pandas df
        count_unique: bool, return a count of the number of unique records with duplicate entries
    """
    def count_unique():

        duplicates = df.duplicated(subset=subset)
        duplicate_idx = duplicates[duplicates==True].index.tolist()  # obtain indices of duplicate data

        dup_df = df.loc[duplicate_idx]                    # obtain duplicate records using indices
        dup_df.head()
        return 'Number of unique records with duplicates: ' + str(dup_df[subset].unique().shape[0])
        
    if count_unique:
        print('Total number of duplicate records : ',df.duplicated(subset=subset).sum())
        print(count_unique())

def remove_duplicates(df,sort_by=list(),subset=''):
    """
    Parameters:
    ----------
    df: pandas df
    sort_by: columns to sort by
    subset: column name to check for duplicates
    
    Returns:
    -------
    dataframe with duplicates removed
    
    """
    temp = df.sort_values(by=sort_by,ascending=False)
    temp.drop_duplicates(subset = [subset],keep='first',inplace=True)
    
    print('Number of records before removing duplicates: ',df.shape[0])
    print('Number of records after removing duplicates: ',temp.shape[0])
    return temp


def convert_install_2_nums(text):
    """
    convert the values from text to integers
   Params:
   -------
   text: raw text input
   
   Returns:
   --------
   interger 
    """
    text = text.replace(',','')
    text = text.replace('+','')
    return int(text)


def sort_bars(df):
    """Sorts the indices of the given dataframe so that bars appear sorted when plotted
    
    Params:
    -------
    df: pandas dataframe
    
    Returns
    -------
    pandas df with sorted indices
    
    """
    num_rows = df.shape[0]
    temp_df = df.reset_index(drop=True)
    indices = [num_rows-1-i for i in range(num_rows)] # reverse number the indices so that the highest y value has the highes index
    temp_df.index = indices
    temp_df.sort_index(ascending=True,inplace=True)
    return temp_df


### === Plotting Functions == ###

def bar_plot(df, ax, x, y,figsize,kind='bar'):
    #if kind='barh'
    plot_obj = df.plot(x=x, y=y, ax=ax, figsize=figsize,kind=kind,sort_columns=True,table=True)
    plot_obj.axhline(y=0,color='black',linewidth=1.0,alpha=0.7)
    plot_obj.xaxis.label.set_visible(False)
    return plot_obj

def barh_plot(df, ax, x, y,figsize=(12,8),kind='barh'):
    #if kind='barh'
    plot_obj = df.plot(x=x, y=y, ax=ax, figsize=figsize,kind=kind,sort_columns=True)
    plot_obj.axvline(x=0,color='black',linewidth=1.0,alpha=0.7)
    plot_obj.xaxis.label.set_visible(False)
    return plot_obj

def get_labels(plot_obj,ylabels=True):
    if ylabels:
        ylabs=[]
        for i in list(plot_obj.get_yticklabels()):
            ylabs.append(i._text)
        return ylabs
    elif not ylabels:
        xlabs=[]
        for i in list(plot_obj.get_xticklabels()):
            xlabs.append(i._text)
        return xlabs
    
def diverging_plot():
    plt.hlines(y=df2.name, xmin=0, xmax=df2.age_z, color=df2.colors, alpha=0.4, linewidth=5)
    
    
### === Functions to format plot style === ###

def do_headings(plot_obj,fig,what=['main_heading','sub_heading'],headings=[]):
    xmin_xmax = plot_obj.get_xlim()
    ymin_ymax =plot_obj.get_ylim()
    
    def main_heading(text):
        
        # heading text
#         plot_obj.text(x = xmin_xmax[0], y = ymin_ymax[1] + 2, s = "The best Apps are for business",
#                           fontsize = 26, weight = 'bold', alpha = .75)
        plot_obj.text(x = 0.0, y = 1, s = text,
                          fontsize = 26, weight = 'bold', alpha = .75,
                     transform=fig.transFigure)
        return plot_obj
    
    def sub_heading(text):
        
        # heading text
#         plot_obj.text(x = xmin_xmax[0], y = ymin_ymax[1] + .5, s = text,
#                           fontsize = 19, alpha = .85)
        plot_obj.text(x = 0.0, y = 0.91, s = text,
                          fontsize = 19, alpha = .85,
                     transform=fig.transFigure)
        return plot_obj
    
    ## do calls here
    if 'main_heading' in what:
            main_heading(headings[0])
    if 'sub_heading' in what:
            sub_heading(headings[1])
            
    return plot_obj

def do_credits(plot_obj,fig):
    xmin_xmax = plot_obj.get_xlim()
    ymin_ymax =plot_obj.get_ylim()
    
    left = '© Amo'
    right = 'Data Source: GooglePlay'
    _ = plot_obj.text(x = 0, y = 0,
                      s=left,fontsize = 14, 
                      weight='bold',
                      color = '#f0f0f0', 
                      backgroundcolor = 'grey',
                      verticalalignment='center',
                      horizontalalignment='center',
                      transform = fig.transFigure,
                      
                 )
    _ = plot_obj.text(x = 0.9, y = 0,
                      s=right,fontsize = 14, 
                      color = '#000000', 
                      
                      verticalalignment='center',
                      horizontalalignment='center',
                      transform = fig.transFigure,
                      
                 )
    
    
def label_bars(plot_obj,df,value_label='percent'):
    ycords = plot_obj.get_yticks().tolist()
    xcords = df[value_label].values.tolist()
    
    xleft =plot_obj.get_xlim()[0] # shift the bars 0.5 units away to the left of the x-axis
    if xleft<0:
        xleft+= 0.5
    elif xleft>0:
        xleft-=0.5
    for i,(j,k) in enumerate(zip(xcords,ycords)):
        _ = plot_obj.text(x=xleft,y=k,s=str(j)+'%', 
                          verticalalignment='baseline',
                         color='#000000',
                          fontsize = 14,
                          
                         )
    return plot_obj


def change_xlim(plot_obj,left):
    
    return plot_obj.set_xlim(left=left,right=plot_obj.get_xlim()[1])
    

def turn_off_labels(plot_obj,axis='x',which='both'):
    return plot_obj.tick_params(axis=axis,which=which,bottom=False,labelbottom=False)

###=== MISC ======= ###
def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])