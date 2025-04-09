
import pandas as pd
import re
from os import path
import tiktoken
import os
import re
import yaml
import logging
import glob
import numpy as np
from yaml.loader import SafeLoader
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import app.archive.blob_fetch_sas_url as sasurl
from app.archive.summary_and_classifier_prompt_template import *
import uuid
import datetime

logger = logging.getLogger(__name__)
logger.info("Check")


AZURE_DI_ENDPOINT = os.getenv("ZZ_AZURE_DI_ENDPOINT")
AZURE_DI_KEY = os.getenv("ZZ_AZURE_DI_KEY")

NUM_SENT_OVERLAP=2
enc = tiktoken.get_encoding("r50k_base")

document_analysis_client = DocumentAnalysisClient(
    endpoint=AZURE_DI_ENDPOINT,
    credential=AzureKeyCredential(AZURE_DI_KEY)
)

class Pre_Processing():

    def __init__(self):
        self.dataframe = pd.DataFrame()
        self.filelist = list()

    def extract_text_form_recognizer(self,file,file_url):
        extracted_text =None
        try:
            if file_url:
                print("...............................",file_url)
                extracted_text = document_analysis_client.begin_analyze_document_from_url('prebuilt-layout',file_url).result()
            else:
                open_file = open(file,'rb').read()
                extracted_text = document_analysis_client.begin_analyze_document('prebuilt-layout',open_file).result()
        except Exception as e:
            logging.info("extraction form recognizer failed",e)
        return extracted_text

    def to_dataframe(self,extracted_text, file_name):

        data = pd.DataFrame(columns=['content','file_name','page_number','xmin','ymin','xmax','ymax','title'])
        doc_title = ''
        try:
            for para in extracted_text.paragraphs:
                content = para.content
                if para.role == "title":
                    doc_title = para.content
                pageNumber = para.bounding_regions[0].page_number
                x_min,y_min = list(para.bounding_regions[0].polygon[0])
                x_max,y_max = list(para.bounding_regions[0].polygon[2])
                coordinate = [x_min,x_max,y_min,y_max]
                #pageNumber,coordinate = _get_cordinate(para.bounding_regions[0])
                x_min,x_max,y_min,y_max = coordinate
                data.loc[len(data)] = [content,file_name,pageNumber,x_min,y_min,x_max,y_max,doc_title]
        except Exception as e:
            logger.info("extracted to_dataframe failed",e)
        return data

    def bounding_box(self,coordinates,idx_map,row,column,page_set):
        try:
            table_coordinate = table_dict = {}
            if coordinates:
                #print(f'Iterating - {coordinates} at {row} & {col}')
                table_coordinate[idx_map[(row,column)]] = list(coordinates)
            axis = ['x-min','y-min','x-max','y-max']
            table_dict['coordinate'] = {}
            axis_count = 0
            for point in range(0,3,2):
                for loc in range(2):
                    table_dict['coordinate'][axis[axis_count]] = table_coordinate[point][loc]
                    axis_count += 1
            table_dict['page_number'] = list(page_set)
            remove_None = lambda row : all(item is None for item in row)
            matrix = [row for row in matrix if not remove_None(row)]
            #table_dict['coordinate'] = table_coordinate
            table_dict['table'] = matrix
        except Exception as e:
            logging.info("bounding box failed",e)
            pass
        return table_dict

    def create_table(self,table):
        try:
            rows, cols = table.row_count, table.column_count
            matrix = [[None] * (cols) for i in range(rows)]
            for content in table.cells:
                row, col = content.row_index, content.column_index
                matrix[row][col] = content.content
        except Exception as e:
            logger.info("create matrix from table failed",e)
        return matrix

    # def save_table(self,table_dict):
    #     matrix = table_dict['matrix']
    #     path_ = path.dirname(path.abspath(input_['document']))
    #     data = pd.DataFrame(matrix)
    #     table_path = path.join(path_,f'table{idx}.xlsx')
    #     data.to_excel(table_path)

    def get_table_coordinate(self,row,col,boundingBox,idx_map):
        if (row,col) in idx_map:
            return boundingBox[idx_map[(row,col)]]
        return []

    def get_relevant_table_index(self, table, idx_map, indx_dict, row_indx, column_indx, table_coordinate):
        max_row=0
        for x in indx_dict.values():
            if x[0]>max_row and x[1]==column_indx:
                max_row=x[0]
        rel_indx=list(indx_dict.keys())[list(indx_dict.values()).index([max_row,column_indx])]
        row=row_indx
        column=column_indx
        boundingBox = table.cells[rel_indx].bounding_regions[0].polygon
        coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)
        if coordinates:
            table_coordinate[idx_map[(row,column)]] = list(coordinates)
        return table_coordinate

    def extract_table(self,table):
        try:
            page_number = list()
            page_set = set()
            table_coordinate = {}
            table_dict = {}
            rows, cols = table.row_count-1, table.column_count-1
            matrix = [[None] * (cols+1) for i in range(rows+1)]
            idx_map = {(0, 0): 0, (0, cols): 1, (rows, cols): 2, (rows, 0): 3}
            indx_dict={}
            for indx in range(0,len(table.cells)):
                cell=table.cells[indx]
                row, column = cell.row_index, cell.column_index
                indx_dict[indx]=[row,column]
                matrix[row][column] = cell.content
                boundingBox = cell.bounding_regions[0].polygon
                page_number = cell.bounding_regions[0].page_number
                page_set.add(page_number)
                coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)
                if coordinates:
                    table_coordinate[idx_map[(row,column)]] = list(coordinates)
                if indx==len(table.cells)-1:
                    if row==rows and column!=cols:
                        table_coordinate=self.get_relevant_table_index(table, idx_map, indx_dict, rows, cols, table_coordinate)
                    elif row!=rows:
                        table_coordinate=self.get_relevant_table_index(table, idx_map, indx_dict, rows, 0, table_coordinate)
                        table_coordinate=self.get_relevant_table_index(table, idx_map, indx_dict, rows, cols, table_coordinate)
                    if 1 not in table_coordinate.keys():
                        rel_row=0
                        for x in indx_dict.values():
                            if x[1]==cols:
                                rel_row=x[0]
                                break
                        rel_indx=list(indx_dict.keys())[list(indx_dict.values()).index([rel_row,cols])]
                        row=0
                        column=cols
                        boundingBox = table.cells[rel_indx].bounding_regions[0].polygon
                        coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)
                        if coordinates:
                            table_coordinate[idx_map[(row,column)]] = list(coordinates)
                    if 0 not in table_coordinate.keys():
                        rel_row=0
                        for x in indx_dict.values():
                            if x[1]==0:
                                rel_row=x[0]
                        rel_indx=list(indx_dict.keys())[list(indx_dict.values()).index([rel_row,0])]
                        row=0
                        column=0
                        boundingBox = table.cells[rel_indx].bounding_regions[0].polygon
                        coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)
                        if coordinates:
                            table_coordinate[idx_map[(row,column)]] = list(coordinates)

            axis = ['x-min','y-min','x-max','y-max']
            table_dict['coordinate'] = {}
            axis_count = 0

            for point in range(0,len(table_coordinate)):
                for loc in range(2):
                    table_dict['coordinate'][axis[axis_count]] = table_coordinate[point][loc]
                axis_count += 1

            if len(page_set)!=0:
                table_dict['page_number'] = list(page_set)
                remove_None = lambda row : all(item is None for item in row)
                matrix = [row for row in matrix if not remove_None(row)]
                #table_dict['coordinate'] = table_coordinate
                table_dict['table'] = matrix
                for i in range(len(table_dict['table'])):
                    for j in range(len(table_dict['table'][i])):
                        if table_dict['table'][i][j] is None:
                            table_dict['table'][i][j]=''
        except Exception as e:
            logger.info("extract table function failed "+ str(e))
            pass
        return table_dict

    def isOverlap(self,content,big_rect):
        try:
            if (content["xmin"] <= big_rect['coordinate']["x-max"] and
                content["xmax"] >= big_rect['coordinate']["x-min"] and
                content["ymin"] <= big_rect['coordinate']["y-max"] and
                content["ymax"] >= big_rect['coordinate']["y-min"]):
                    return True
            return False
        except Exception as e:
            return False

    def update_table_info(self,dataframe,table_dict):

        df_r = pd.DataFrame()
        try:
            data = dataframe.copy()
            if len(table_dict['page_number']) > 1:
                raise ValueError('Page Number has 2 values')
            page_number = table_dict['page_number'][0]
            if page_number:
                page_df = data[data.page_number==page_number]
                page_df = self.get_table_idx(page_df,table_dict)
                idx = list(page_df.index)
                if len(idx)!=0:
                    idx_s,idx_e = idx[0],idx[-1]
                    table_content = '\n'.join([','.join(rows) for rows in table_dict['table'] if None not in rows] )
                    table_content = f"\n<table-start> \n\n {table_content} \n\n <table-end>\n"
                    row_dict = {'content':table_content,'page_number':page_number,
                            'xmin':table_dict['coordinate']['x-min'],
                            'ymin':table_dict['coordinate']['y-min'],
                            'xmax':table_dict['coordinate']['x-max'],
                            'ymax':table_dict['coordinate']['y-max']}
                    df_r = pd.concat([data.iloc[:idx_s], pd.DataFrame(row_dict, index=[idx_s]), data.iloc[idx_e+1:]], ignore_index=True)
                    return df_r
                else:
                    return dataframe
        except Exception as e:
            logger.info("update table info function got failed",e)
            return dataframe

    def get_table_idx(self,page_df,table_dict):
        return page_df[page_df.apply(self.isOverlap,big_rect=table_dict,axis=1)]

    def get_token_length(self,content):
        content_encode = enc.encode(content)
        return len(content_encode)

    def do_overlap_para(self,R1, R2):
        if (R1[0]>=R2[2]) or (R1[2]<=R2[0]) or (R1[3]<=R2[1]) or (R1[1]>=R2[3]):
            return False
        else:
            return True

    def get_chunks(self,data_update, file_name,chunk_size):
        try:
            doc_df = pd.DataFrame(columns=['content','page_number'])
            threshold = chunk_size
            print("Thresold seet is ")
            print(threshold)
            for page_num in data_update['page_number'].unique():
                appended_text = []
                page_df = data_update[data_update['page_number'] == page_num]
                page_df.reset_index(drop=True, inplace=True)

                current_len = 0
                current_text = ''

                for i, row in page_df.iterrows():
                    if current_len + row['token_len'] <= threshold:
                        current_text += row['content'] + ' '
                        current_len += row['token_len']
                    else:
                        appended_text.append(current_text.strip())
                        current_text = row['content'] + ' '
                        current_len = row['token_len']
                appended_text.append(current_text.strip())

                if len(appended_text)>1:
                    for text in appended_text:
                        doc_df.loc[len(doc_df)] = [text,page_num]
                else:
                    doc_df.loc[len(doc_df)] = [appended_text[0],page_num]
            doc_df['file_name'] = file_name
            doc_df['token_len'] = doc_df['content'].apply(self.get_token_length)
        except Exception as e:
            logger.info("chunking function failed",e)
        return doc_df

    def get_chunks_appr_overlap(self,data_update,file_name,chunk_size):
            try:
                doc_df = pd.DataFrame(columns=['content','page_number'])
                threshold = chunk_size

                for page_num in data_update['page_number'].unique():
                    appended_text = []
                    page_df = data_update[data_update['page_number'] == page_num]
                    page_df.reset_index(drop=True, inplace=True)
                    current_len = 0
                    current_text = ''
                    for i, row in page_df.iterrows():

                        if current_len + row['token_len'] <= threshold:
                            current_text += row['content'] + ' '
                            current_len += row['token_len']

                        else:
                            appended_text.append(current_text.strip())
                            sent_list = re.split("\.", current_text.strip())
                            temp_text=current_text
                            current_len = 0
                            current_text = ''
                            if len(sent_list[-1])==0:
                                sent_list=sent_list[:-1]
                            if len(sent_list)>=NUM_SENT_OVERLAP:
                                for x in range(NUM_SENT_OVERLAP):
                                    current_text+=sent_list[len(sent_list)+x-NUM_SENT_OVERLAP].strip()
                                    # current_len += self.get_token_length(current_text)
                            else:
                                current_text=temp_text
                            current_text =current_text+' '+ row['content']
                            current_len = self.get_token_length(current_text)
                    appended_text.append(current_text.strip())

                    if len(appended_text)>1:
                        for text in appended_text:
                            doc_df.loc[len(doc_df)] = [text,page_num]

                    else:
                        doc_df.loc[len(doc_df)] = [appended_text[0],page_num]
                doc_df['token_len'] = doc_df['content'].apply(self.get_token_length)
                doc_df['file_name'] = file_name
            except Exception as e:
                logger.info("chunking function failed",e)
            return doc_df

    def para_alignment(self,dataframe):
        try:
            df_left=pd.DataFrame(columns=dataframe.columns)
            df_right=pd.DataFrame(columns=dataframe.columns)
            df_aligned=pd.DataFrame(columns=dataframe.columns)
            for page_num in dataframe['page_number'].unique():
                df_left=df_left.iloc[0:0]
                df_right=df_right.iloc[0:0]
                page_df = dataframe[dataframe['page_number'] == page_num]
                page_df.reset_index(drop=True, inplace=True)
                xmin,ymin,xmax,ymax=page_df.loc[0,'xmin'],page_df.loc[0,'ymin'],page_df.loc[0,'xmax'],page_df.loc[0,'ymax']
                for i, row in page_df.iterrows():
                    if row['xmin']>xmax:
                        df_right=pd.concat([df_right,row.to_frame().T])
                    elif self.do_overlap_para([xmin,ymin,xmax,ymax],[row['xmin'],row['ymin'],row['xmax'],row['ymax']]):
                        df_left=pd.concat([df_left,row.to_frame().T])
                    else:
                        df_left=pd.concat([df_left,row.to_frame().T])
                        xmin,ymin,xmax,ymax=row['xmin'],row['ymin'],row['xmax'],row['ymax']
                df=pd.concat([df_left,df_right],axis=0)
                df_aligned=pd.concat([df_aligned,df],axis=0)
            return df_aligned

        except Exception as e:
            logger.info("paragraph alignment function failed",e)

    def get_chunks_multiple_pages(self,data_update, file_name,chunk_size):
        try:
            doc_df = pd.DataFrame(columns=['content','file_name','page_number','token_len','title','word_length','file_url','publication_date','document_source_id', "company_name",'industry_name'])
            threshold = chunk_size

            page_num=[]
            current_len = 0
            word_len =0
            current_text = ''
            title_list =[]
            data_update.reset_index(drop=True, inplace=True)
            data_update.fillna('', inplace=True)
            logger.info("inside get chunk multiple page function")
            for i, row in data_update.iterrows():

                if current_len + row['token_len'] <= threshold:
                    current_text += row['content'] + ' '
                    current_len += row['token_len']

                    if len(row['title'])>0:
                        title_list.append(row['title'])
                    page_num.append(str(row['page_number']))

                else:
                    logger.info("inside else part of get chunk multiple process")
                    doc_df.loc[len(doc_df.index)] = [current_text,file_name,','.join(np.unique(np.array(page_num))),current_len, ', '.join(list(set(title_list)))
                                                     ,data_update['word_length'].iloc[0],data_update['file_url'].iloc[0],data_update['publication_date'].iloc[0],
                                                     data_update['document_source_id'].iloc[0],data_update['company_name'].iloc[0],data_update['industry_name'].iloc[0]]
                    title_list.clear()
                    current_text = row['content'] + ' '
                    current_len = row['token_len']

                    title_list.append(row['title'])
                    page_num.clear()
            logger.info("completed else of get chunk multiple process")
            doc_df.loc[len(doc_df.index)] = [current_text,file_name,','.join(np.unique(np.array(page_num))),current_len, ', '.join(list(set(title_list)))
                                             ,data_update['word_length'].iloc[0],data_update['file_url'].iloc[0],data_update['publication_date'].iloc[0],
                                             data_update['document_source_id'].iloc[0],data_update['company_name'].iloc[0],data_update['industry_name'].iloc[0]]

        except Exception as e:
            logger.info("chunking function failed",e)

        return doc_df

    def datetime_format(self):
        logger.info("########### Date time generated ##########")
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        return formatted_datetime

def pdf_to_df(folder_with_pdfs,container_client,Container,storage_account_name,storage_account_key): #,connection_string,Container,storage_account_name,storage_account_key

    data_updates = pd.DataFrame()
    out = Pre_Processing()
    text_data_for_publication_date =[]
    complete_file_text_list=[]
    complete_file_text= None
    final_dataframe_text=pd.DataFrame(columns=['content','file_name','page_number','token_len','title','word_length', 'file_url','publication_date','document_source_id',
                                               "company_name",'industry_name'])
    try:
        for pdf_file in os.listdir(folder_with_pdfs):
            if pdf_file.endswith('.pdf'):
                pdf_file_path = os.path.join(folder_with_pdfs, pdf_file)
                print("Processing " + str(pdf_file_path))
                document_source_id = out.datetime_format().split('.')[-1]+'-'+ str(uuid.uuid4())
                #check if file in blob otherwise comment sas url line

                blob_sas_url = sasurl.blobUrl.blob_sas_token(container_client,Container,storage_account_name,storage_account_key,pdf_file)
                extracted_text = out.extract_text_form_recognizer(pdf_file_path,file_url=None)
                data_updates = out.to_dataframe(extracted_text,pdf_file_path)
                tables =extracted_text.tables
                try:
                    for table in tables:
                        table_dict = out.extract_table(table)
                        if 'page_number' in table_dict.keys():
                            data_updates = out.update_table_info(data_updates,table_dict)

                    if len(data_updates)!=0:
                        data_updates = out.para_alignment(data_updates)

                except Exception as e :
                    print("Exception in pdf_to_df",str(e))
                    pass
                print('para_alignment',data_updates.columns)

                if 'content' in data_updates.columns:
                    data_updates['token_len'] = data_updates['content'].apply(out.get_token_length)
                    for text in data_updates['content'].values:
                        complete_file_text_list.append(text)
                    file_word_length = str(len((" ".join(map(str,complete_file_text_list))).split(" ")))

                    data_updates['word_length'] = file_word_length

                    for _, row in data_updates.iterrows():
                        if int(row['page_number'])<=4:
                            text_data_for_publication_date.append(row['content'])

                    complete_file_text =  "\n".join(map(str,text_data_for_publication_date))

                    publication_date =  publication_date_prompt(complete_file_text)

                    publication_date = publication_date.replace('-','_').replace(":", "_").replace("/", "_")

                    if len(publication_date)>10:
                        datetime.datetime.strptime(publication_date,'%d_%b_%Y').strftime('%d_%m_%Y')

                    data_updates['publication_date'] = publication_date

                    company_industry_details_dict = company_industry_prompt(complete_file_text)
                    data_updates['company_name'] = company_industry_details_dict['company_name']
                    data_updates['industry_name'] = company_industry_details_dict['industry_name']
                    logger.info("#### publication date and industry prompt completed ########")
                    data_updates['file_name'] = pdf_file
                    data_updates['file_url'] = str(blob_sas_url)
                    data_updates['document_source_id'] = document_source_id
                    data_updates = data_updates[data_updates.token_len>0]
                    final_dataframe_text=pd.concat([final_dataframe_text,data_updates],axis=0)

    except Exception as e:
        print("Exception in pdf_to_df",str(e))
        logger.info("prerocessing main function failed",e)

    return final_dataframe_text

def pdf_to_df_from_blob_file(file_url):
    complete_file_text =None
    complete_file_text_list= []
    token_len_sum = 0
    file_name = file_url.split("?")[0].split('/')[-1]
    data_updates = pd.DataFrame()
    out = Pre_Processing()
    final_dataframe_text=pd.DataFrame(columns=['content','file_name','page_number','token_len','title','word_length'])

    try:
        if str(file_name).endswith('.pdf'):
            print("Processing " + str(file_name))
            extracted_text = out.extract_text_form_recognizer(file=None,file_url=file_url)

            data_updates = out.to_dataframe(extracted_text,file_name)
            tables =extracted_text.tables
            try:
                for table in tables:
                    table_dict = out.extract_table(table)

                    if 'page_number' in table_dict.keys():
                        data_updates = out.update_table_info(data_updates,table_dict)

                if len(data_updates)!=0:
                    data_updates = out.para_alignment(data_updates)

            except Exception as e :
                print("Exception in pdf_to_df",str(e))
                pass
            print('para_alignment',data_updates.columns)
            if 'content' in data_updates.columns:
                data_updates['token_len'] = data_updates['content'].apply(out.get_token_length)
                data_updates['file_name'] = file_name
                # data_updates['file_url'] = blob_sas_url
                data_updates = data_updates[data_updates.token_len>0]

                final_dataframe_text=pd.concat([final_dataframe_text,data_updates],axis=0)
                final_dataframe_text = final_dataframe_text[['content','token_len']]

                for text in final_dataframe_text['content'].values:
                    complete_file_text_list.append(text)

                complete_file_text = "\n".join(map(str,complete_file_text_list))
                token_len_sum = final_dataframe_text['token_len'].sum()

                print('final_dataframe_text token sum',token_len_sum)
    except Exception as e:
        logger.info("prerocessing main function failed",e)

    return complete_file_text,token_len_sum


def divide_chunks(data_df,chunk_size,redis_obj):
    response_dict = {}
    result_df = pd.DataFrame()
    try:
        out = Pre_Processing()
        result_df=pd.DataFrame(columns=['content','file_name','page_number','token_len','title','word_length','file_url',"publication_date",'document_source_id',
                                           "company_name",'industry_name'])
        print("Result DF before divide")
        print(data_df.info())

        for file_name in data_df['file_name'].unique():
            print(file_name)
            ## Different Methods go here!
            result_df=pd.concat([result_df,out.get_chunks_multiple_pages(data_df[data_df["file_name"] == file_name].reset_index(),file_name,chunk_size )],axis=0)
        print("Completed all chunk & batch for size " + str(chunk_size))
        print(result_df.info())

    except Exception as e:
        for file in data_df['file_name'].unique():
            redis_obj.response_failure_status(file ,str(chunk_size),error=str(e))
        response_dict.update({'Error':str(e)})

    return result_df, response_dict