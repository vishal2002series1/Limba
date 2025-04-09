import re
import logging
import datetime
import numpy as np
import pandas as pd
import tiktoken

logger = logging.getLogger(__name__)

enc = tiktoken.get_encoding("r50k_base")
no_of_sent_overlap = 2

class Pre_Processing():
    def __init__(self, DOC_INTEL_CLIENT):
        self.dataframe = pd.DataFrame()
        self.filelist = list()
        self.DOC_INTEL_CLIENT = DOC_INTEL_CLIENT

    def extract_text_form_recognizer(self, model_id, file):
        try:
            extracted_text = self.DOC_INTEL_CLIENT.begin_analyze_document(model_id, file).result()
        except Exception as e:
            logger.exception("Error in extract_text_form_recognizer")
            return None
        return extracted_text

    def to_dataframe(self, extracted_text, file_name):
        data = pd.DataFrame(columns=['content', 'file_name', 'page_number', 'xmin', 'ymin', 'xmax', 'ymax', 'title'])
        doc_title = ''
        try:
            for para in extracted_text.paragraphs:
                content = para.content
                if para.role == "title":
                    doc_title = para.content
                pageNumber = para.bounding_regions[0].page_number
                x_min, y_min = list(para.bounding_regions[0].polygon[0])
                x_max, y_max = list(para.bounding_regions[0].polygon[2])
                coordinate = [x_min, x_max, y_min, y_max]
                x_min, x_max, y_min, y_max = coordinate

                data.loc[len(data)] = [content, file_name, pageNumber, x_min, y_min, x_max, y_max, doc_title]

        except Exception as e:
            logger.exception("Error in to_dataframe")
        return data

    def create_table(self, table):
        try:
            rows, cols = table.row_count, table.column_count
            matrix = [[None] * cols for i in range(rows)]

            for content in table.cells:
                row, col = content.row_index, content.column_index
                matrix[row][col] = content.content

        except Exception as e:
            logger.exception("Error in create_table")
        return matrix

    def get_table_coordinate(self, row, col, boundingBox, idx_map):
        if (row, col) in idx_map:
            return boundingBox[idx_map[(row, col)]]
        return []

    def get_relevant_table_index(self, table, idx_map, indx_dict, row_indx, column_indx, table_coordinate):
        max_row = 0
        for x in indx_dict.values():
            if x[0] > max_row and x[1] == column_indx:
                max_row = x[0]
        rel_indx = list(indx_dict.keys())[list(indx_dict.values()).index([max_row, column_indx])]
        row = row_indx
        column = column_indx
        boundingBox = table.cells[rel_indx].bounding_regions[0].polygon

        coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)
        if coordinates:
            table_coordinate[idx_map[(row, column)]] = list(coordinates)
        return table_coordinate

    def extract_table(self, table):
        try:
            page_number = list()
            page_set = set()
            table_coordinate = {}
            table_dict = {}
            rows, cols = table.row_count - 1, table.column_count - 1

            matrix = [[None] * (cols + 1) for i in range(rows + 1)]

            idx_map = {(0, 0): 0, (0, cols): 1, (rows, cols): 2, (rows, 0): 3}
            indx_dict = {}

            for indx in range(len(table.cells)):
                cell = table.cells[indx]

                row, column = cell.row_index, cell.column_index
                indx_dict[indx] = [row, column]
                matrix[row][column] = cell.content

                boundingBox = cell.bounding_regions[0].polygon
                page_number = cell.bounding_regions[0].page_number
                page_set.add(page_number)

                coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)

                if coordinates:
                    table_coordinate[idx_map[(row, column)]] = list(coordinates)

                if indx == len(table.cells) - 1:
                    if row == rows and column != cols:
                        table_coordinate = self.get_relevant_table_index(table, idx_map, indx_dict, rows, cols, table_coordinate)

                    elif row != rows:
                        table_coordinate = self.get_relevant_table_index(table, idx_map, indx_dict, rows, 0, table_coordinate)
                        table_coordinate = self.get_relevant_table_index(table, idx_map, indx_dict, rows, cols, table_coordinate)

                    if 1 not in table_coordinate.keys():
                        rel_row = 0
                        for x in indx_dict.values():
                            if x[1] == cols:
                                rel_row = x[0]
                                break
                        rel_indx = list(indx_dict.keys())[list(indx_dict.values()).index([rel_row, cols])]
                        row = 0
                        column = cols
                        boundingBox = table.cells[rel_indx].bounding_regions[0].polygon
                        coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)
                        if coordinates:
                            table_coordinate[idx_map[(row, column)]] = list(coordinates)

                    if 0 not in table_coordinate.keys():
                        rel_row = 0
                        for x in indx_dict.values():
                            if x[1] == 0:
                                rel_row = x[0]
                        rel_indx = list(indx_dict.keys())[list(indx_dict.values()).index([rel_row, 0])]
                        row = 0
                        column = 0
                        boundingBox = table.cells[rel_indx].bounding_regions[0].polygon
                        coordinates = self.get_table_coordinate(row, column, boundingBox, idx_map)
                        if coordinates:
                            table_coordinate[idx_map[(row, column)]] = list(coordinates)

            axis = ['x-min', 'y-min', 'x-max', 'y-max']

            table_dict['coordinate'] = {}

            axis_count = 0
            for point in range(len(table_coordinate)):
                for loc in range(2):
                    table_dict['coordinate'][axis[axis_count]] = table_coordinate[point][loc]
                axis_count += 1

            if len(page_set) != 0:
                table_dict['page_number'] = list(page_set)

                remove_None = lambda row: all(item is None for item in row)

                matrix = [row for row in matrix if not remove_None(row)]
                table_dict['table'] = matrix

                for i in range(len(table_dict['table'])):
                    for j in range(len(table_dict['table'][i])):
                        if table_dict['table'][i][j] is None:
                            table_dict['table'][i][j] = ''

        except Exception as e:
            logger.exception("Error in extract_table")
        return table_dict

    def isOverlap(self, content, big_rect):
        try:
            if (content["xmin"] <= big_rect['coordinate']["x-max"] and
                content["xmax"] >= big_rect['coordinate']["x-min"] and
                content["ymin"] <= big_rect['coordinate']["y-max"] and
                content["ymax"] >= big_rect['coordinate']["y-min"]):
                return True
            return False
        except Exception as e:
            logger.exception("Error in isOverlap")
            return False

    def update_table_info(self, dataframe, table_dict):
        df_r = pd.DataFrame()
        try:
            data = dataframe.copy()
            if len(table_dict['page_number']) > 1:
                raise ValueError('Page Number has 2 values')
            page_number = table_dict['page_number'][0]
            if page_number:
                page_df = data[data.page_number == page_number]
                page_df = self.get_table_idx(page_df, table_dict)
                idx = list(page_df.index)
                if len(idx) != 0:
                    idx_s, idx_e = idx[0], idx[-1]
                    table_content = '\n'.join([','.join(rows) for rows in table_dict['table'] if None not in rows])
                    table_content = f"\n<table-start> \n\n {table_content} \n\n <table-end>\n"
                    row_dict = {'content': table_content, 'page_number': page_number,
                                'xmin': table_dict['coordinate']['x-min'],
                                'ymin': table_dict['coordinate']['y-min'],
                                'xmax': table_dict['coordinate']['x-max'],
                                'ymax': table_dict['coordinate']['y-max']}
                    df_r = pd.concat([data.iloc[:idx_s], pd.DataFrame(row_dict, index=[idx_s]), data.iloc[idx_e + 1:]], ignore_index=True)
                    return df_r
                else:
                    return dataframe
        except Exception as e:
            logger.exception("Error in update_table_info")
            return dataframe

    def get_table_idx(self, page_df, table_dict):
        try:
            return page_df[page_df.apply(self.isOverlap, big_rect=table_dict, axis=1)]
        except Exception as e:
            logger.exception("Error in get_table_idx")
            return pd.DataFrame()

    def get_token_length(self, content):
        try:
            content_encode = enc.encode(content)
            return len(content_encode)
        except Exception as e:
            logger.exception("Error in get_token_length")
            return 0

    def do_overlap_para(self, R1, R2):
        try:
            if (R1[0] >= R2[2]) or (R1[2] <= R2[0]) or (R1[3] <= R2[1]) or (R1[1] >= R2[3]):
                return False
            else:
                return True
        except Exception as e:
            logger.exception("Error in do_overlap_para")
            return False

    def get_chunks(self, data_update, file_name, CHUNK_SIZE):
        try:
            doc_df = pd.DataFrame(columns=['content', 'page_number'])
            threshold = CHUNK_SIZE

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

                if len(appended_text) > 1:
                    for text in appended_text:
                        doc_df.loc[len(doc_df)] = [text, page_num]
                else:
                    doc_df.loc[len(doc_df)] = [appended_text[0], page_num]

            doc_df['file_name'] = file_name
            doc_df['token_len'] = doc_df['content'].apply(self.get_token_length)
        except Exception as e:
            logger.exception("Error in get_chunks")
        return doc_df

    def get_chunks_appr_overlap(self, data_update, file_name, CHUNK_SIZE):
        try:
            doc_df = pd.DataFrame(columns=['content', 'page_number'])
            threshold = CHUNK_SIZE

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
                        temp_text = current_text
                        current_len = 0
                        current_text = ''
                        if len(sent_list[-1]) == 0:
                            sent_list = sent_list[:-1]
                        if len(sent_list) >= no_of_sent_overlap:
                            for x in range(no_of_sent_overlap):
                                current_text += sent_list[len(sent_list) + x - no_of_sent_overlap].strip()
                        else:
                            current_text = temp_text
                        current_text = current_text + ' ' + row['content']
                        current_len = self.get_token_length(current_text)
                appended_text.append(current_text.strip())

                if len(appended_text) > 1:
                    for text in appended_text:
                        doc_df.loc[len(doc_df)] = [text, page_num]
                else:
                    doc_df.loc[len(doc_df)] = [appended_text[0], page_num]
            doc_df['token_len'] = doc_df['content'].apply(self.get_token_length)
            doc_df['file_name'] = file_name
        except Exception as e:
            logger.exception("Error in get_chunks_appr_overlap")
        return doc_df

    def para_alignment(self, dataframe):
        try:
            df_left = pd.DataFrame(columns=dataframe.columns)
            df_right = pd.DataFrame(columns=dataframe.columns)
            df_aligned = pd.DataFrame(columns=dataframe.columns)
            for page_num in dataframe['page_number'].unique():
                df_left = df_left.iloc[0:0]
                df_right = df_right.iloc[0:0]
                page_df = dataframe[dataframe['page_number'] == page_num]
                page_df.reset_index(drop=True, inplace=True)
                xmin, ymin, xmax, ymax = page_df.loc[0, 'xmin'], page_df.loc[0, 'ymin'], page_df.loc[0, 'xmax'], page_df.loc[0, 'ymax']
                for i, row in page_df.iterrows():
                    if row['xmin'] > xmax:
                        df_right = pd.concat([df_right, row.to_frame().T])
                    elif self.do_overlap_para([xmin, ymin, xmax, ymax], [row['xmin'], row['ymin'], row['xmax'], row['ymax']]):
                        df_left = pd.concat([df_left, row.to_frame().T])
                    else:
                        df_left = pd.concat([df_left, row.to_frame().T])
                        xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
                df = pd.concat([df_left, df_right], axis=0)
                df_aligned = pd.concat([df_aligned, df], axis=0)
            return df_aligned

        except Exception as e:
            logger.exception("Error in para_alignment")

    def get_chunks_multiple_pages(self, data_update, file_name, CHUNK_SIZE):
        try:
            doc_df = pd.DataFrame(columns=['chunk_content', 'doc_name', 'chunk_doc_pages', 'chunk_token_len', 'chunk_titles', 'doc_word_length', 'doc_url', 'doc_path', 'doc_details', 'doc_id', 'tags'])
            page_num = []
            current_len = 0
            word_len = 0
            current_text = ''
            title_list = []
            data_update.reset_index(drop=True, inplace=True)
            data_update.fillna('', inplace=True)
            for i, row in data_update.iterrows():

                if current_len + row['token_len'] <= int(CHUNK_SIZE):
                    current_text += row['content'] + ' '
                    current_len += row['token_len']
                    if len(row['title']) > 0:
                        title_list.append(row['title'])
                    page_num.append(int(row['page_number']))
                else:
                    doc_df.loc[len(doc_df.index)] = [current_text, file_name, list(map(int, list(np.unique(np.array(page_num))))), current_len, list(set(title_list)), data_update['doc_word_length'].iloc[0], data_update['doc_url'].iloc[0], data_update['doc_path'].iloc[0], data_update['doc_details'].iloc[0], data_update['doc_id'].iloc[0], data_update['tags'].iloc[0]]
                    title_list.clear()
                    page_num.clear()
                    current_text = row['content'] + ' '
                    current_len = row['token_len']
                    title_list.append(row['title'])
                    page_num.append(int(row['page_number']))
            doc_df.loc[len(doc_df.index)] = [current_text, file_name, list(map(int, list(np.unique(np.array(page_num))))), current_len, list(set(title_list)), data_update['doc_word_length'].iloc[0], data_update['doc_url'].iloc[0], data_update['doc_path'].iloc[0], data_update['doc_details'].iloc[0], data_update['doc_id'].iloc[0], data_update['tags'].iloc[0]]

        except Exception as e:
            logger.exception("Error in get_chunks_multiple_pages")
        return doc_df

    def datetime_format(self):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return formatted_datetime
