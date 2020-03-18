'''
This is Tailored to the specific data format of equipment in my department, you can (and should modify) this\
to your requirement.
'''


import pandas as pd
import numpy as np
import scipy as sp

class XRD_line(pd.DataFrame):
    '''Read the XRD line of a sample'''
    Name=None
    
    def __init__(self, filename=None, **kwargs):
        
        
        array=None
        with open(filename,'r',encoding='utf-8') as f:
            
            self.Name = f.readline().strip('\n')
            
        # reading datas
            line=f.readline().strip('\n')
            while line != '':
                array=update_numpy(array, np.array([line.split()]))
                line=f.readline().strip('\n')
                
            super().__init__(data=array, columns=['2-Theta','Intensity'], dtype='float64',**kwargs)



class Raman_line(pd.DataFrame):
    '''Reaad the Raman line of a sample'''
    Name=None
    
    def __init__(self, filename=None, **kwargs):
        
        
        array=None
        with open(filename,'r',encoding='utf-8') as f:
            
            self.Name = f.readline().strip('\n')
            
        # reading datas
            line=f.readline().strip('\n')
            while line != '':
                array=update_numpy(array, np.array([line.split()]))
                line=f.readline().strip('\n')
                
            super().__init__(data=array, columns=['Raman shift(cm-1)','Intensity'], dtype='float64',**kwargs)




class PDF(pd.DataFrame):
    ''' Read & process the PDF data\
        Key notes:\
        to save: self.to_csv()'''
    PDF_number=None
    Structure_name=None
    Chemical_name=None
    
    def __init__(self,filename=None):
        array=[]

        with open(filename,'r',encoding='utf-8') as f:
        
            self.PDF_number = f.readline().strip('\n\t')
            self.Structure_name= f.readline().strip('\n\t')
            self.Chemical_name=f.readline().strip('\n\t')
            
            
            line=f.readline()
            
        
            while '2-Theta' not in line:
                line = f.readline()
            
            columns=line.strip('\n').strip().split('  ')
            columns.remove('')
            columns[1]='d(10$^{-10}$ m)'
       
       
        
            line=f.readline().strip('\n').strip()
        
            while line != '':
                line=line.split('  ')
            
                while '' in line:
                    line.remove('')
            
               # print(line)
                for i, entry in enumerate(line):
                
                    if i != 3:
                        line[i]=float(entry)
                    
                try:
                    line[7]
                except:
                    line.append(np.NaN)
            
                array.append(line)
            
            
                line=f.readline().strip('\n').strip()
               
        
      
            super().__init__(array, columns=columns)
            
    
            
    def drop_lines(self,*args,factor=1,base_height=0,**kwargs):
            
        from matplotlib import collections as matcoll
            
            
        lines=[]
        for l in range(len(self[self.columns[0]])):
            pair=[(self[self.columns[0]][l],base_height),(self[self.columns[0]][l],
                  self[self.columns[2]][l]*factor+base_height)]
            lines.append(pair)
      
        dpL=matcoll.LineCollection(lines,*args,**kwargs)
    
      
        return dpL
            



    
    

class ReadingTGA(pd.DataFrame):
    '''Return a Dataframe of TGA data'''
    size=None
    
    def __init__(self,filename=None):
        signals=[]
        array=None
    
        with open(filename,'r',encoding='utf-16') as f:
        
            line = f.readline()
        
            while 'Size' not in line:
                line=f.readline()
            
            self.size=float(line.split().pop(1))
        
            while 'Sig' not in line:
                line = f.readline()
        
     
        
            while 'Sig' in line:
                signals.append(line.strip('\n').split('\t')[-1])
                line = f.readline()
                
                
            signals[2]='Weight(%)'
            
            while 'OrgFile'  not in line:
                line=f.readline()
        
                        
       
          
            # read data
            line=f.readline().strip('\n')
            while line != '':
            
                array=update_numpy(array, np.array([line.split()]))
                line=f.readline().strip('\n')
            
        
            
            super().__init__(array, columns=signals, dtype='float64')
            
            # calculate the weight percentage
            self[self.columns[2]]=self[self.columns[2]]/self.size*100
        
           
    
    
class Impedence(pd.DataFrame):
    '''Read the impedence data of the file'''
    def __init__(self,filename=None,**kwargs):
        array=None
        signals=[]
    
        with open(filename,'r', encoding='utf-8') as f:
            line=f.readline()
            while 'Pt.' not in line:
                line=f.readline()
                
            s_t=line.strip('\n').split('\t')
            
            for sig in s_t:
                signals.append(sig.strip('""'))
           
            signals=signals[1:4]
            signals.append('-Z_2')
            
            
            line=f.readline().strip('\n')
            while line != '':
                new_line=line.split()[1:4]+[line.split()[-1]]
                array=update_numpy(array, np.array([new_line]))
                line=f.readline().strip('\n')
                
            
          
            
            
        super().__init__(data=array,columns=signals, dtype='float64',**kwargs)
        
        self[self.columns[-1]]=self[self.columns[-1]]*(-1)
        
            
            

class CV(pd.DataFrame):
    '''A subclass of DataFrame for CV object'''
    def __init__(self,filename=None,mass=1.0,**kwargs):
        '''Return a DataFrame of GV curve'''
        array=None
        
        
        with open(filename,'r',encoding='utf-8') as f:
            line = f.readline()
            while 'Title' not in line:
                line = f.readline()
            
        # parameter(title, etc.)
           
        
            
            parameters=line.strip('\n').split('\t')[1].strip("''").split(',')
            
            scan_rate=parameters[2]
           
            
            line = f.readline()
            while '"' not in line:
                line = f.readline()
             
        # signals
            s_t=line.strip('\n').split('\t')
            signals=[]
            for sig in s_t:
                signals.append(sig.strip('""'))
                
         
        # reading datas
            line=f.readline().strip('\n')
            while line != '':
                array=update_numpy(array, np.array([line.split()]))
                line=f.readline().strip('\n')
            super().__init__(data=array, columns=signals, dtype='float64',**kwargs)
            
        
        
        
        self.mass=mass
        self[self.columns[1]]=self[self.columns[1]]/self.mass
            
        
        self.scan_rate=scan_rate
        
     
        
        self.mass=mass
        
        
    def charge_amount(self):
        '''The amount of charge being transfered during a charge/discharge\
           circle (i.e. charge transfered in charging process is roughly one half\
           of the charge amount)'''
        
        return np.trapz(self[self.columns[1]], 
                        x=self[self.columns[0]])*1000/float(self.scan_rate.strip('mV/S'))
    
    
    
    def Capacitance(self,massfactor=1):
        '''massfactor: transform between the mass/volume capacitance'''
        r_w=self[self.columns[0]].idxmax()
        l_w=self[self.columns[0]].idxmin()
        
        voltage_window=self.iloc[r_w,0]-self.iloc[l_w,0]
        
        cap_df=pd.DataFrame([[float(self.scan_rate.strip('mV/S')),self.charge_amount()/voltage_window/2/massfactor]],
                              columns=['Scan rate', 'Capacitance'])
        # around one half of the charge is transfered during charge/discharge
        return cap_df
            
       
    
 


class GV(pd.DataFrame):
    '''A subclass of DataFrame'''
    def __init__(self,filename=None,mass=1.0,accuracy=2,**kwargs):
        '''Return a DataFrame of GV curve'''
        array=None
    
        with open(filename,'r',encoding='utf-8') as f:
            line = f.readline()
            while 'Title' not in line:
                line = f.readline()
            
        # parameter(title, etc.)
           
        
            
            p=line.strip('\n').split('\t')
            absolute_c=float(p[1].strip('[]').split(',')[0].strip('A'))
           
            
            line = f.readline()
            while '"' not in line:
                line = f.readline()
             
        # signals
            s_t=line.strip('\n').split('\t')
            signals=[]
            for sig in s_t:
                signals.append(sig.strip('""'))
                
         
        # reading datas
            line=f.readline().strip('\n')
            while line != '':
                array=update_numpy(array, np.array([line.split()]))
                line=f.readline().strip('\n')
            super().__init__(data=array, columns=signals, dtype='float64',**kwargs)
            
        t_column=self.columns[0]
        self[t_column]=self[t_column]-self[t_column][0]
            
        
        self.current=round(absolute_c/float(mass),accuracy)
        
        self.t_column=self.columns[0]
        self.v_column=self.columns[1]
    
        
    def charge_curve(self):
        '''Returns a charge curve'''
            # critical point
        c=self[self.columns[1]].idxmax()
    
    # create dataframe for charge & discharge respectively
        char=self.truncate(after=c)
            
        return char
        
        
        
        
    def discharge_curve(self):
        '''Returns a discharge curve'''
        c=self[self.v_column].idxmax()
        
       
        
        dischar=self.truncate(before=c)
        
        dischar=dischar.reset_index(drop=True)
        
    
         
            
        dischar[self.t_column]=dischar[self.t_column]-dischar[self.t_column][0]
        
            
        return dischar
        
        
    def Capacitance(self):
        '''Calculate the capacitance by Dataframe, return a Dataframe object
        with currents and capacitance'''
    
        dischar=self.discharge_curve()
    
   
        time=dischar.iloc[-1,0]
        voltage=dischar.iloc[0,1]-dischar.iloc[-1,1]
       
        capacitance=time*self.current/voltage
            
        cap_df=pd.DataFrame([[self.current,capacitance]],columns=['Current', 'Capacitance'])
            
    
        return cap_df
    
    def work_power(self):
        '''Return a Dataframe of work (Wh) and power (W) values'''
        
        dischar=self.discharge_curve()
        
        # energy of the electrode/device:
        w=np.trapz(dischar[self.v_column], x=dischar[self.t_column]*self.current)/3600
        # power of the lectrode/device:
        p=w*3600/dischar.iloc[-1,0]
        
        
        return pd.DataFrame([[w,p]],columns=['Energy density', 'Power density'])
    
    
    
    
def update_numpy(array,new_line):
    try:
        array=np.concatenate((array,np.array(new_line)),axis=0)
        
    except:
        array=np.array(new_line)
        
    return array
            
if __name__=='__main__':
    pdf=PDF(filename='test/9.txt')
    pdf.head()
       
                
                
            
        
