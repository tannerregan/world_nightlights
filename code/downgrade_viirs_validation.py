#imports
import rasterio, pandas, seaborn
from matplotlib import pyplot as plt    
from matplotlib.colors import LogNorm
from scipy.ndimage.filters import uniform_filter, gaussian_filter
from rasterio import warp
import statsmodels.formula.api as smf
from statsmodels.tools.eval_measures import rmse
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

#functions---------------------------------------------------------------------
def open_data(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,year):
    dmsp_o=rasterio.open(dmsp_f.format(y=year))   
    viirs_o=rasterio.open(viirs_f.format(y=year)) #need to downsample first
    gasm_o=rasterio.open(afr_gas)   
    afrm_o=rasterio.open(afr_bff)   
    argn_o=rasterio.open(afr_rgn)  

    #dmsp and regions as array
    dmsp_a=dmsp_o.read(1)
    argn_a=argn_o.read(1)
        
    #mask as array: combine two masks as one (mask is 1 if gas flares=1 or africa land=0)
    mask_a=((gasm_o.read(1)==1) | (afrm_o.read(1)==0)) 
    
    #viirs as arrays: resample VIIRS to DMSP resolution, do this for four types of resampling (mean=5)
    viirs_b=rasterio.band(viirs_o,1)
    new_prf=afr_prf.copy()
    new_prf.update(
        dtype=viirs_b.dtype,)
    viirs_a=[]
    for stat in [5]:
        tmp_f=jdir+"viirs_rsmp_{s}.tif".format(s=stat)
        with rasterio.open(tmp_f, 'w', **new_prf) as out_dst:
            destination=rasterio.band(out_dst,1)
            warp.reproject(viirs_b,destination,dst_transform=new_prf['transform'],dst_crs=new_prf['crs'],dst_nodata=new_prf['nodata'], resampling=stat)
        viirs_a.append(rasterio.open(tmp_f).read(1))
            
    open_names=["DMSP", "VIIRS_mn", "Africa Regions", "mask"]
    open_arrays=[dmsp_a, viirs_a[0], argn_a, mask_a]
    stacked=np.stack(open_arrays,axis=0) 
    for a in open_arrays:
        del a
        
    #Add x,y to identify each cell
    grid=np.stack((np.meshgrid(np.arange(dmsp_o.width), np.arange(dmsp_o.height)))) #add a grid of coordinates, same size as input raster
    stacked=np.concatenate((stacked,grid),axis=0) 
    open_names.append('x')
    open_names.append('y')
    
    return stacked, open_names

def data_to_frame(stacked,col_names):
    columns=np.transpose(np.reshape(stacked,(len(col_names),-1)))
    df=pandas.DataFrame(columns, columns=col_names)
    df=df[(df['mask']==0)]  #exclude gas and Africa masked areas    
    df=df.drop(['mask'], axis=1)
    return df

def add_gaus_filters(data,names):
    #Ensure that we use VIIRS for the filter
    viirs_loc_in_list=1
    if names[viirs_loc_in_list]!='VIIRS_mn':
        raise NameError('VIIRS_mn in wrong place of stacked arrays!')
    #Gaussian filter with optimal syrian parameters
    w=13
    s=1.9  #sigma defaults to 1.9: roughly the average optimal sigma from our replication of li et al 2017
    t=(((w - 1)/2)-0.5)/s #convert the window size to the ‘truncated’ value that the function accepts as an input
    filter_g=gaussian_filter(data[viirs_loc_in_list], sigma=s, truncate=t)
    data=np.concatenate((data,filter_g[None,:, :,]), axis=0) #Need to add a new dimension to filter
    names.append('VIIRS_mn_gaus')
        
    return data,names

def create_viirs_pctiles(data):
    #create percentiles (ignoring VIIRS<1, set 0<>1 to -1 and <0 to -2)
    data['VIIRS_mn_pctiles']=pandas.qcut(data.loc[(data['VIIRS_mn']>=1),'VIIRS_mn'], 100, labels=False) #ignore zeroes
    data.loc[(data['VIIRS_mn']<1),'VIIRS_mn_pctiles']=-1
    data.loc[(data['VIIRS_mn']<=0),'VIIRS_mn_pctiles']=-2
    return data

def calc_rmse(x1,x2):
    rmse=(((x1-x2)**2).mean())**0.5
    return rmse

    
def log_plus_2(x):
    return np.log(x + 2.0)

def save_to_file(in_a,out_f,prf):
    with rasterio.open(out_f, 'w', **prf) as dst:
        dst.write(in_a, 1)  

def syrian_approach(b,s,a,w,viirs_a,mask_a,prf,fn):  
    t=(((w - 1)/2)-0.5)/s #convert the window size to the ‘truncated’ value that the function accepts as an input
    viirs_a[(viirs_a<0)]=0 #need to set negative viirs to 0
    Z=gaussian_filter(viirs_a**b, sigma=s, truncate=t) #Generate matrices Z=G(X,b)*M(s,w)
    dmsp_hat=a*Z
    dmsp_hat[(mask_a==1)]=0 #set mask
    dmsp_hat[(dmsp_hat>63)]=63 #topcode
    dmsp_hat[(dmsp_hat<0)]=0 #bottomcode
    dmsp_hat=np.around(dmsp_hat, decimals=0) #round to integer
    dmsp_hat=dmsp_hat.astype(np.uint8) #store as integer
    save_to_file(dmsp_hat,fn,prf)
    
def syrian_main(year,b,s,a,w):
    stacked_inputs,stacked_names=open_data(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,year=year)
    viirs_a=stacked_inputs[1]
    if stacked_names[1]!='VIIRS_mn':
        raise NameError('VIIRS_mn in wrong place of stacked arrays!')
    mask_a=stacked_inputs[6]
    if stacked_names[6]!='mask':
        raise NameError('mask in wrong place of stacked arrays!')
    del stacked_inputs, stacked_names
    syrian_approach(b=b,
                    s=s,
                    a=a,
                    w=w,
                    viirs_a=viirs_a,
                    mask_a=mask_a,
                    prf=afr_prf,
                    fn=dgvval_f.format(y=year,m="lietal"))

def write_predictions_to_raster(df,prf,fn):
    pix_fix=df.to_numpy() #DF needs to be in order: x,y,z
    shape_out=(prf['height'],prf['width'])
    dmsp_hat = 0 * np.empty(shape=shape_out)
    dmsp_hat[pix_fix.transpose()[1].astype(int), pix_fix.transpose()[0].astype(int)] = pix_fix.transpose()[2]
    dmsp_hat[(dmsp_hat>63)]=63 #topcode
    dmsp_hat[(dmsp_hat<0)]=0 #bottomcode
    dmsp_hat=np.around(dmsp_hat, decimals=0) #round to integer
    dmsp_hat=dmsp_hat.astype(np.uint8) #store as integer
    save_to_file(dmsp_hat,fn,prf)   
    
def est_OLS(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,year):
    #open data
    stacked_inputs,stacked_names=open_data(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,year)
    #add spatial filters
    stacked_inputs,stacked_names=add_gaus_filters(stacked_inputs,stacked_names)
    df=data_to_frame(stacked_inputs,stacked_names)
    df=create_viirs_pctiles(df)
    del stacked_inputs,stacked_names
    df=df[['DMSP','VIIRS_mn','VIIRS_mn_gaus','VIIRS_mn_pctiles']]
    
    ols_model='DMSP ~ log_plus_2(VIIRS_mn) * log_plus_2(VIIRS_mn_gaus) + np.power(log_plus_2(VIIRS_mn), 2) * log_plus_2(VIIRS_mn_gaus)'
    pctile_lst=[p for p in df.VIIRS_mn_pctiles.unique()]
    model_lst=[]
    for pctile in pctile_lst:
        mdl_3= smf.ols(formula=ols_model, data=df.loc[df.VIIRS_mn_pctiles==pctile,:]).fit()
        model_lst.append(mdl_3)
    
    return pctile_lst, model_lst

def prd_OLS(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,pctile_lst, model_lst,year):
    #open data
    stacked_inputs,stacked_names=open_data(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,year)
    #add spatial filters
    stacked_inputs,stacked_names=add_gaus_filters(stacked_inputs,stacked_names)
    df=data_to_frame(stacked_inputs,stacked_names)
    df=create_viirs_pctiles(df)
    del stacked_inputs,stacked_names
    df=df[['VIIRS_mn','VIIRS_mn_gaus','VIIRS_mn_pctiles','x','y']]
    
    for i,pctile in enumerate(pctile_lst):
        mdl_3=model_lst[i]
        df.loc[df.VIIRS_mn_pctiles==pctile,'dmsp_hat']=mdl_3.predict(df.loc[df.VIIRS_mn_pctiles==pctile,:])
    
    write_predictions_to_raster(df=df[['x','y','dmsp_hat']],
                                prf=afr_prf,
                                fn=dgvval_f.format(y=year,m="OLS"))

def open_df_for_analysis(dmsp_f,afr_gas,afr_bff,dgvval_f,year):
    dmsp_a=rasterio.open(dmsp_f.format(y=year)).read(1)     
    mask_a=((rasterio.open(afr_gas).read(1) ==1) | (rasterio.open(afr_bff).read(1) ==0)) 
    
    ntr_a=rasterio.open(gdir+"/downgrade_viirs_validation/simDMSP2013_cln.tif").read(1)  
    syr_a=rasterio.open(dgvval_f.format(y=year,m="lietal")).read(1)  
    ols_a=rasterio.open(dgvval_f.format(y=year,m="OLS")).read(1)  
    etr_a=rasterio.open(dgvval_f.format(y=year,m="ETR")).read(1)  
    ebl_a=rasterio.open(dgvval_f.format(y=year+'blfix',m="ETR")).read(1)  
    dvn_a=rasterio.open(gdir+"/clean_dvnl/DVNL{y}.tif".format(y=year)).read(1)  
    
    stacked=np.stack([dmsp_a,mask_a,ntr_a,syr_a,ols_a,etr_a,ebl_a,dvn_a],axis=0) 
    df=data_to_frame(stacked,['DMSP','mask','DMSP_ntr','DMSP_syr','DMSP_ols','DMSP_etr','DMSP_ebl', 'DVNL'])
    if year=='2012':
        df=df.drop(['DMSP_ntr'],axis=1)
        df=df.drop(['DVNL'],axis=1)
        
    return df


def confusion_matrix(df,i,hat,lbl,y):
    tupu=((df['DMSP']==0) & (df[hat]==0)).sum()
    tupl=((df['DMSP']==0) & (df[hat]>0)).sum()
    tlpl=((df['DMSP']>0) & (df[hat]>0)).sum()
    tlpu=((df['DMSP']>0) & (df[hat]==0)).sum()
    recall=tlpl/(tlpl+tlpu) #recall is the share of all truly lit pixels correctly classified as lit
    precision=tlpl/(tlpl+tupl) #precision is the share of all predicted lit pixels correctly classified as lit
    F1=2*precision*recall/(precision+recall)
    cnfmtr = pandas.DataFrame( 
            [[tupu,tupl],
            [tlpu,tlpl]])
    cnfmtr = cnfmtr.rename(columns={0: 'unlit',1: 'lit'}, index={0: 'unlit', 1: 'lit'})
    
    fig, ax = plt.subplots(figsize=(9,9))
    seaborn.set(font_scale=1)
    plt.figure(figsize=(10,7))
    ax=seaborn.heatmap(cnfmtr, annot=True, annot_kws={'size': 20}, 
                    fmt=",.0f",
                    cbar=False,
                    cmap=ListedColormap(['white']),
                    linewidths=2,
                    linecolor='black'
                    )
    ax.set_xlabel('Predicted: {}'.format(lbl),fontsize=20,fontweight ='bold')
    ax.set_ylabel('True: DMSP (bloom fix)'.format(lbl),fontsize=20,fontweight ='bold')
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    plt.subplots_adjust(bottom =0.275)
    plt.gcf().text(0.05, 0.1, r'Recall={:.2f}, Precision={:.2f}, F1 score={:.2f}'.format(recall,precision,F1), fontsize=18)
    plt.savefig(home+"/figures/data"+y+"_cnfmtr "+lbl+".png")

def make_histograms(df,i,hat,lbl,y):
    Nzeroes=(df[hat]==0).sum()
    textstr = r'N zeroes (not shown)={:,}'.format(Nzeroes)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.25)
    
    f, ax = plt.subplots(figsize=(7, 5))
    plt.hist(df.loc[df[hat]>0,hat], bins=64,range=(0,64), label=[lbl])
    ax.text(0.05,0.95, textstr, transform=ax.transAxes, fontsize=10,verticalalignment='top', bbox=props)
    ax.set_ylim([0, 700000])
    ax.legend(prop={'size': 10})
    plt.savefig(home+"/figures/data"+y+"_histo"+str(i)+".png")

def make_scatter(df,i,hat,lbl,y):
    seaborn.set(rc={'axes.facecolor':'white'}) #set all graphs to have white background
    prediction_rmse = rmse(df['DMSP'], df[hat]) 
    int_rmse = rmse(df['DMSP'].loc[(df['DMSP']>0) & (df[hat]>0)], df[hat].loc[(df['DMSP']>0) & (df[hat]>0)]) 
    textstr = '\n'.join((
        r'RMSE=%.3f' % (prediction_rmse, ),
        r'RMSE (lit only)=%.3f' % (int_rmse, )
        ))
    
    props = dict(boxstyle='round', facecolor='none', alpha=0.5)
    
    hm_df=df[['DMSP',hat]]
    hm_df['counts']=1
    hm_df = hm_df.pivot_table(index=hat,columns= "DMSP",values='counts', aggfunc=np.sum)
    max_dn=np.array([df[hat].max(),df['DMSP'].max()]).max()
    for dn in range(max_dn):
        if dn not in hm_df.columns:
            hm_df[dn] = np.nan
        if dn not in hm_df.index:
            hm_df=hm_df.reindex(hm_df.index.values.tolist()+[dn])
        
    hm_df=hm_df.sort_index()
    hm_df = hm_df[sorted(hm_df.columns.tolist())]
    
    #ytick_lst=[dn for dn in range(max_dn)]
    #for l,dn in enumerate(ytick_lst): #create 13 unique equally separated integers starting at zero
    #    if dn % round(max_dn/13)  != 0:
    #        ytick_lst[l]="" 
    ticks=[]
    for i in range(61):
        if int(i/5)*5==i:
            ticks.append(i)
        else:
            ticks.append(None)
    fig, ax = plt.subplots(figsize=(9,9))
    seaborn.heatmap(hm_df, cmap='Blues', square=True, norm=LogNorm(),
                    xticklabels=ticks,yticklabels=ticks, cbar=False)
    ax.invert_yaxis()
    fig.text(0.15,0.85, textstr, fontsize=20,
                verticalalignment='top', bbox=props)
    #ax.set_title('Scatter predicted ('+lbl+') vs DMSP')
    #ax.set(xlabel='DMSP', ylabel='Predicted DMSP: {}'.format(lbl))
    ax.set_xlabel('DMSP (bloom fix)',fontsize=20,fontweight ='bold')
    ax.set_ylabel('Predicted DMSP: {}'.format(lbl),fontsize=20,fontweight ='bold')
    plt.ylim(0,61)
    plt.yticks(fontsize=18)
    plt.xticks(fontsize=18)
    plt.plot([0,64], [0, 64], color='black', linewidth=0.5)
    mean_at_true=df[['DMSP',hat]].groupby('DMSP').mean()
    mean_at_true['x']=mean_at_true.index+0.5
        
    plt.scatter(x=mean_at_true['x'], y=mean_at_true[hat], color='red',s=1.5)
    plt.savefig(home+"/figures/data"+y+"_sctr "+lbl+".png",bbox_inches='tight')

def open_df_for_analysis_extras(in_f,method,afr_gas,afr_bff,dgvval_f,year):
    dmsp_a=rasterio.open(in_f).read(1)     
    mask_a=((rasterio.open(afr_gas).read(1) ==1) | (rasterio.open(afr_bff).read(1) ==0)) 
    etr_a=rasterio.open(dgvval_f.format(y=year+method,m="ETR")).read(1)  
    
    stacked=np.stack([dmsp_a,mask_a,etr_a],axis=0) 
    df=data_to_frame(stacked,['DMSP','mask','DMSP_'+method+'_etr'])
    
    return df

def sum_of_NL(in_f,afr_gas,afr_bff):
    dmsp_a=rasterio.open(in_f).read(1)     
    mask_a=((rasterio.open(afr_gas).read(1) ==1) | (rasterio.open(afr_bff).read(1) ==0)) 
    return np.ma.array(dmsp_a, mask=mask_a).sum()

#------------------------------------------------------------------------------  
#This code downgrades VIIRS to DMSP for 2012 and 2013 to do validation analysis
#Create out-of-sample DMSP predictions for 2012 and 2013 by:
    #1. Nature (2013) only
    #2. Syria
    #3. OLS
    #4. ExtraTrees
#Run anlayses between true and predicted DMSP 
    #RMSE and scatter
    #lit/unlit comparisons and histograms of lit cells

#------------------------------------------------------------------------------
#Create out-of-sample DMSP predictions for 2012 and 2013-----------------------

#1. Nature 2013 is already available in clean DMSP as /clean_dmsp/DMSP2013sim_cln.tif

#2. Syria re-optimised---------------------------------------------------------
#optimal parameters using 2012 data from March 25, 2021: b,s,a,w=0.3436, 2.0141999999999998, 23.07370121203281, 13
##syrian_main(year='2013',b=0.3436,s=2.0141999999999998,a=23.07370121203281,w=13)
#optimal parameters using 2013 data from March 25, 2021: b,s,a,w=0.3636, 1.8142, 21.335030135739903, 13
##syrian_main(year='2012',b=0.3636,s=1.8142,a=21.335030135739903,w=13)


#3. OLS------------------------------------------------------------------------
#estimate using 2012
pctile_lst, model_lst=est_OLS(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,year='2012')
#predict using 2013
prd_OLS(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,pctile_lst, model_lst,year='2013')

#estimate using 2013
pctile_lst, model_lst=est_OLS(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,year='2013')
#predict using 2012
prd_OLS(dmsp_f,viirs_f,afr_gas,afr_bff,afr_rgn,pctile_lst, model_lst,year='2012')


#4. ExtraTrees 2012 and 2013 are already available in /downgrade_viirs_validation/




#------------------------------------------------------------------------------
#Run anlayses between true and predicted DMSP----------------------------------
"""
#for year 2013-----------------------------------------------------------------
df=open_df_for_analysis(dmsp_f,afr_gas,afr_bff,dgvval_f,year='2013')

#hat_lst=['DMSP','DMSP_ntr','DMSP_syr','DMSP_ols','DMSP_etr', 'DVNL']
#hat_lbl_lst=['DMSP','Li et al.','Syrian','OLS','ETR', 'Nechaev et al.']
hat_lst=['DMSP_ntr','DMSP_etr','DMSP_ebl', 'DVNL']
hat_lbl_lst=['Li et al.','ETR', 'ETR (bloom fix)', 'Nechaev et al.']


#confusion matrices
#add stats for precision, recall, and F1
for i,hat in enumerate(hat_lst):
    if i>0:
        lbl=hat_lbl_lst[i]
        confusion_matrix(df,i,hat,lbl,y='2013')


#scatter with RMSE
for i,hat in enumerate(hat_lst):
    if i>0:
        lbl=hat_lbl_lst[i]
        make_scatter(df,i,hat,lbl,y='2013')
"""

#for year 2013 (compare to blooming correction)--------------------------------
df=open_df_for_analysis(dmsp_bl_f,afr_gas,afr_bff,dgvval_f,year='2013')



hat_lst=['DMSP','DMSP_ntr','DMSP_etr','DMSP_ebl', 'DVNL']
hat_lbl_lst=['DMSP','Li et al.','ETR', 'ETR (bloom fix)', 'Nechaev et al.']


#confusion matrices
#add stats for precision, recall, and F1
for i,hat in enumerate(hat_lst):
    if i>0:
        lbl=hat_lbl_lst[i]
        confusion_matrix(df,i,hat,lbl,y='2013')

#scatter with RMSE
for i,hat in enumerate(hat_lst):
    if i>0:
        lbl=hat_lbl_lst[i]
        make_scatter(df,i,hat,lbl,y='2013')


"""
#for year 2012-----------------------------------------------------------------
df=open_df_for_analysis(dmsp_f,afr_gas,afr_bff,dgvval_f,year='2012')

hat_lst=['DMSP','DMSP_syr','DMSP_ols','DMSP_etr']
hat_lbl_lst=['DMSP','Syrian','OLS','ETR']

seaborn.set(rc={'axes.facecolor':'white'}) #set all graphs to have white background

#confusion matrices
#add stats for precision, recall, and F1
for i,hat in enumerate(hat_lst):
    if i>0:
        lbl=hat_lbl_lst[i]
        confusion_matrix(df,i,hat,lbl,y='2012')

#histograms (drop zeroes, but add stat for number of zeroes)
for i,hat in enumerate(hat_lst):
    lbl=hat_lbl_lst[i]
    make_histograms(df,i,hat,lbl,y='2012')
    
#scatter with RMSE
for i,hat in enumerate(hat_lst):
    if i>0:
        lbl=hat_lbl_lst[i]
        make_scatter(df,i,hat,lbl,y='2012')

#Comparison of other (blooming, topcoding, and both fixes) DMSP types----------
#blooming
for y in ['2012','2013']:
    df=open_df_for_analysis_extras(dmsp_bl_f.format(y=y),'blfix',afr_gas,afr_bff,dgvval_f,y)
    confusion_matrix(df,i='x1',hat='DMSP_blfix_etr',lbl='ETR blfix',y=y)
    make_scatter(df,i='x1',hat='DMSP_blfix_etr',lbl='ETR blfix',y=y)
#topcoding
for y in ['2012','2013']:
    df=open_df_for_analysis_extras(dmsp_tc_f.format(y=y),'tcfix',afr_gas,afr_bff,dgvval_f,y)
    confusion_matrix(df,i='x2',hat='DMSP_tcfix_etr',lbl='ETR tcfix',y=y)
    make_scatter(df,i='x2',hat='DMSP_tcfix_etr',lbl='ETR tcfix',y=y)
#both
for y in ['2012','2013']:
    df=open_df_for_analysis_extras(dmsp_bltc_f.format(y=y),'bltcfix',afr_gas,afr_bff,dgvval_f,y)
    confusion_matrix(df,i='x3',hat='DMSP_bltcfix_etr',lbl='ETR bltcfix',y=y)
    make_scatter(df,i='x3',hat='DMSP_bltcfix_etr',lbl='ETR bltcfix',y=y)
"""
    

#Graph timeseries of sum of NLs------------------------------------------------

year_lst=[y for y in range(1992,2020+1)]
nl_cln_lst=[]
nl_bl_lst=[]
nl_tc_lst=[]
nl_bltc_lst=[]
for year in year_lst:
    sum_nl=sum_of_NL(dmsp_f.format(y=year),afr_gas,afr_bff)
    nl_cln_lst.append(sum_nl)
    
    sum_nl=sum_of_NL(dmsp_bl_f.format(y=year),afr_gas,afr_bff)
    nl_bl_lst.append(sum_nl)
    
    sum_nl=sum_of_NL(dmsp_tc_f.format(y=year),afr_gas,afr_bff)
    nl_tc_lst.append(sum_nl)
    
    sum_nl=sum_of_NL(dmsp_bltc_f.format(y=year),afr_gas,afr_bff)
    nl_bltc_lst.append(sum_nl)

seaborn.set() #turn default seaborn grid back on
fig, ax = plt.subplots(figsize=(9,9))
plt.plot(year_lst, nl_cln_lst)
plt.axvline(x=2013.5,linewidth=0.5,color='black', linestyle='dashed')
plt.savefig(home+"/figures/timeseries_cln.png")
fig, ax = plt.subplots(figsize=(9,9))
plt.plot(year_lst, nl_bl_lst)
plt.axvline(x=2013.5,linewidth=0.5,color='black', linestyle='dashed')
plt.savefig(home+"/figures/timeseries_bl.png")
fig, ax = plt.subplots(figsize=(9,9))
plt.plot(year_lst, nl_tc_lst)
plt.axvline(x=2013.5,linewidth=0.5,color='black', linestyle='dashed')
plt.savefig(home+"/figures/timeseries_tc.png")
fig, ax = plt.subplots(figsize=(9,9))
plt.plot(year_lst, nl_bltc_lst)
plt.axvline(x=2013.5,linewidth=0.5,color='black', linestyle='dashed')
plt.savefig(home+"/figures/timeseries_bltc.png")
        
      
#Add a count of topcoded pixels for each year (1992-2013)----------------------
gasm_o=rasterio.open(afr_gas)   
afrm_o=rasterio.open(afr_bff)   
mask_a=((gasm_o.read(1)==1) | (afrm_o.read(1)==0))
tot_pix=np.count_nonzero(mask_a==0)

year_lst=[y for y in range(1992,2013+1)]
tc55_shr_lst=[]
tc55_litshr_lst=[]
tc60_shr_lst=[]
tc60_litshr_lst=[]

for year in year_lst:
    dmsp_o=rasterio.open(dmsp_f.format(y=year))   
    dmsp_a=dmsp_o.read(1)
    tc55_pix=np.count_nonzero(dmsp_a[mask_a==0] >55)
    tc55_shr_lst.append(tc55_pix/tot_pix)
    
    lit_pix=np.count_nonzero(dmsp_a[mask_a==0] >0)
    tc55_litshr_lst.append(tc55_pix/lit_pix)
    
    tc60_pix=np.count_nonzero(dmsp_a[mask_a==0] >60)
    tc60_shr_lst.append(tc60_pix/tot_pix)
    
    lit_pix=np.count_nonzero(dmsp_a[mask_a==0] >0)
    tc60_litshr_lst.append(tc60_pix/lit_pix)
 

df = pandas.DataFrame(list(zip(year_lst,tc55_shr_lst,tc55_litshr_lst,tc60_shr_lst,tc60_litshr_lst)),
               columns =['Year','Share of total >55','Share of lit >55','Share of total >60','Share of lit >60'])
df.T.to_csv(home+"/figures/list_shrpix_topcode.csv")


#Add a count of UNLIT pixels for each year (1992-2013)----------------------
gasm_o=rasterio.open(afr_gas)   
afrm_o=rasterio.open(afr_bff)   
mask_a=((gasm_o.read(1)==1) | (afrm_o.read(1)==0))
tot_pix=np.sum(mask_a==False)

year_lst=[y for y in range(1992,2013+1)]
ul_shr_lst=[]
ul_bl_shr_lst=[]

for year in year_lst:
    #Original DMSP data
    dmsp_o=rasterio.open(dmsp_f.format(y=year))   
    dmsp_a=dmsp_o.read(1)
    ul_pix=np.sum(dmsp_a[mask_a==False]==0)
    ul_shr_lst.append(ul_pix/tot_pix)
    
    #Blooming corrected DMSP data
    dmsp_o=rasterio.open(dmsp_bl_f.format(y=year))   
    dmsp_a=dmsp_o.read(1)
    ul_pix=np.sum(dmsp_a[mask_a==False]==0)
    ul_bl_shr_lst.append(ul_pix/tot_pix)
 

df = pandas.DataFrame(list(zip(year_lst,ul_shr_lst,ul_bl_shr_lst)),
               columns =['Year','Share of total unlit (DMSP)','Share of total unlit (bloom corrected DMSP)'])
df.T.to_csv(home+"/figures/list_shrpix_unlit.csv")





#END---------------------------------------------------------------------------