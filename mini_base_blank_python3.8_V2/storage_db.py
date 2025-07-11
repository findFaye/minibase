# -----------------------------------------------------------------------
# storage_db.py
# Author: Jingyu Han  hjymail@163.com
# -----------------------------------------------------------------------
# the module is to store tables in files
# Each table is stored in a separate file with the suffix ".dat".
# For example, the table named moviestar is stored in file moviestar.dat 
# -----------------------------------------------------------------------

# struct of file is as follows, each block is 4096
# ---------------------------------------------------
# block_0|block_1|...|block_n
# ----------------------------------------------------------------
from common_db import BLOCK_SIZE

# structure of block_0, which stores the meta information and field information
# ---------------------------------------------------------------------------------
# block_id                                # 0
# number_of_dat_blocks                    # at first it is 0 because there is no data in the table
# number_of_fields or number_of_records   # the total number of fields for the table
# -----------------------------------------------------------------------------------------


# the data type is as follows
# ----------------------------------------------------------
# 0->str,1->varstr,2->int,3->bool
# ---------------------------------------------------------------


# structure of data block, whose block id begins with 1
# ----------------------------------------
# block_id       
# number of records
# record_0_offset         # it is a pointer to the data of record
# record_1_offset
# ...
# record_n_offset
# ....
# free space
# ...
# record_n
# ...
# record_1
# record_0
# -------------------------------------------

# structre of one record
# -----------------------------
# pointer                     #offset of table schema in block id 0
# length of record            # including record head and record content
# time stamp of last update  # for example,1999-08-22
# field_0_value
# field_1_value
# ...
# field_n_value
# -------------------------


import struct
import os
import ctypes


# --------------------------------------------
# the class can store table data into files
# functions include insert, delete and update
# --------------------------------------------

class Storage(object):

    # ------------------------------
    # constructor of the class
    # input:
    #       tablename
    # -------------------------------------
    def __init__(self, tablename):
        # print "__init__ of ",Storage.__name__,"begins to execute"
        tablename.strip()

        self.record_list = []
        self.record_Position = []

        if not os.path.exists(tablename + '.dat'.encode('utf-8')):  # the file corresponding to the table does not exist
            print('table file '.encode('utf-8') + tablename + '.dat does not exists'.encode('utf-8'))
            self.f_handle = open(tablename + '.dat'.encode('utf-8'), 'wb+')
            self.f_handle.close()
            self.open = False
            print(tablename + '.dat has been created'.encode('utf-8'))

        self.f_handle = open(tablename + '.dat'.encode('utf-8'), 'rb+')
        print('table file '.encode('utf-8') + tablename + '.dat has been opened'.encode('utf-8'))
        self.open = True

        self.dir_buf = ctypes.create_string_buffer(BLOCK_SIZE)
        self.f_handle.seek(0)
        self.dir_buf = self.f_handle.read(BLOCK_SIZE)

        self.dir_buf.strip()
        my_len = len(self.dir_buf)
        self.field_name_list = []
        beginIndex = 0

        if my_len == 0:  # there is no data in the block 0, we should write meta data into the block 0
            if isinstance(tablename, bytes):
                self.num_of_fields = input(
                    "please input the number of feilds in table " + tablename.decode('utf-8') + ":")
            else:
                self.num_of_fields = input(
                    "please input the number of feilds in table " + tablename + ":")
            if int(self.num_of_fields) > 0:

                self.dir_buf = ctypes.create_string_buffer(BLOCK_SIZE)
                self.block_id = 0
                self.data_block_num = 0
                struct.pack_into('!iii', self.dir_buf, beginIndex, 0, 0,
                                 int(self.num_of_fields))  # block_id,number_of_data_blocks,number_of_fields

                beginIndex = beginIndex + struct.calcsize('!iii')

                # the following is to write the field name,field type and field length into the buffer in turn
                for i in range(int(self.num_of_fields)):
                    field_name = input("please input the name of field " + str(i) + " :")

                    if len(field_name) < 10:
                        field_name = ' ' * (10 - len(field_name.strip())) + field_name

                    while True:
                        field_type = input(
                            "please input the type of field(0-> str; 1-> varstr; 2-> int; 3-> boolean) " + str(
                                i) + " :")
                        if int(field_type) in [0, 1, 2, 3]:
                            break

                    # to need further modification here
                    field_length = input("please input the length of field " + str(i) + " :")
                    temp_tuple = (field_name, int(field_type), int(field_length))
                    self.field_name_list.append(temp_tuple)
                    if isinstance(field_name, str):
                        field_name = field_name.encode('utf-8')

                    struct.pack_into('!10sii', self.dir_buf, beginIndex, field_name, int(field_type),
                                     int(field_length))
                    beginIndex = beginIndex + struct.calcsize('!10sii')

                self.f_handle.seek(0)
                self.f_handle.write(self.dir_buf)
                self.f_handle.flush()

        else:  # there is something in the file

            self.block_id, self.data_block_num, self.num_of_fields = struct.unpack_from('!iii', self.dir_buf, 0)

            print('number of fields is ', self.num_of_fields)
            print('data_block_num', self.data_block_num)
            beginIndex = struct.calcsize('!iii')

            # the followins is to read field name, field type and field length into main memory structures
            for i in range(self.num_of_fields):
                field_name, field_type, field_length = struct.unpack_from('!10sii', self.dir_buf,
                                                                          beginIndex + i * struct.calcsize(
                                                                              '!10sii'))  # i means no memory alignment

                temp_tuple = (field_name, field_type, field_length)
                self.field_name_list.append(temp_tuple)
                print("the " + str(i) + "th field information (field name,field type,field length) is ", temp_tuple)
        # print self.field_name_list
        record_head_len = struct.calcsize('!ii10s')
        record_content_len = sum(map(lambda x: x[2], self.field_name_list))
        # print record_content_len

        Flag = 1
        while Flag <= self.data_block_num:
            self.f_handle.seek(BLOCK_SIZE * Flag)
            self.active_data_buf = self.f_handle.read(BLOCK_SIZE)
            self.block_id, self.Number_of_Records = struct.unpack_from('!ii', self.active_data_buf, 0)
            print('Block_ID=%s,   Contains %s data' % (self.block_id, self.Number_of_Records))
            # There exists record
            if self.Number_of_Records > 0:
                for i in range(self.Number_of_Records):
                    self.record_Position.append((Flag, i))
                    offset = \
                        struct.unpack_from('!i', self.active_data_buf,
                                           struct.calcsize('!ii') + i * struct.calcsize('!i'))[
                            0]
                    record = struct.unpack_from('!' + str(record_content_len) + 's', self.active_data_buf,
                                                offset + record_head_len)[0]
                    tmp = 0
                    tmpList = []
                    for field in self.field_name_list:
                        t = record[tmp:tmp + field[2]].strip()
                        tmp = tmp + field[2]
                        if field[1] == 2:
                            t = int(t)
                        if field[1] == 3:
                            t = bool(t)
                        tmpList.append(t)
                    self.record_list.append(tuple(tmpList))
            Flag += 1

    # ------------------------------
    # return the record list of the table
    # input:
    #       
    # -------------------------------------
    def getRecord(self):
        return self.record_list

    # --------------------------------
    # to insert a record into table
    # param insert_record: list
    # return: True or False
    # -------------------------------
    def insert_record(self, insert_record):

        # example: ['xuyidan','23','123456']

        # step 1 : to check the insert_record is True or False

        tmpRecord = []
        '''
        XXTong Edit 2025.05.25
        Change the record to bytes and write to file
        utf-8 encoding is used for storing data in bytes
        '''
        for idx, field in enumerate(self.field_name_list):
            value = insert_record[idx].strip()
            if field[1] in [0, 1]:  # string types
                if len(value) > field[2]:
                    return False
                tmpRecord.append(value.encode('utf-8'))
            elif field[1] == 2:  # integer type
                try:
                    tmpRecord.append(int(value))
                except ValueError:
                    return False
            elif field[1] == 3:  # boolean type
                try:
                    tmpRecord.append(bool(value))
                except ValueError:
                    return False

            # Pad the value for file storage
            insert_record[idx] = value.ljust(field[2])

        inputstr = ''.join(insert_record)
        self.record_list.append(tuple(tmpRecord))

        for idx in range(len(self.field_name_list)):
            insert_record[idx] = insert_record[idx].strip()
            if self.field_name_list[idx][1] == 0 or self.field_name_list[idx][1] == 1:
                if len(insert_record[idx]) > self.field_name_list[idx][2]:
                    return False
                tmpRecord.append(insert_record[idx])
            if self.field_name_list[idx][1] == 2:
                try:
                    tmpRecord.append(int(insert_record[idx]))
                except:
                    return False
            if self.field_name_list[idx][1] == 3:
                try:
                    tmpRecord.append(bool(insert_record[idx]))
                except:
                    return False
            insert_record[idx] = ' ' * (self.field_name_list[idx][2] - len(insert_record[idx])) + insert_record[idx]

        # step2: Add tmpRecord to record_list ; change insert_record into inputstr
        inputstr = ''.join(insert_record)

        self.record_list.append(tuple(tmpRecord))

        # Step3: To calculate MaxNum in each Data Blocks
        record_content_len = len(inputstr)
        record_head_len = struct.calcsize('!ii10s')
        record_len = record_head_len + record_content_len
        MAX_RECORD_NUM = (BLOCK_SIZE - struct.calcsize('!i') - struct.calcsize('!ii')) / (
                record_len + struct.calcsize('!i'))

        # Step4: To calculate new record Position
        if not len(self.record_Position):
            self.data_block_num += 1
            self.record_Position.append((1, 0))
        else:
            last_Position = self.record_Position[-1]
            if last_Position[1] == MAX_RECORD_NUM - 1:
                self.record_Position.append((last_Position[0] + 1, 0))
                self.data_block_num += 1
            else:
                self.record_Position.append((last_Position[0], last_Position[1] + 1))

        last_Position = self.record_Position[-1]

        # Step5: Write new record into file xxx.dat
        # update data_block_num
        self.f_handle.seek(0)
        self.buf = ctypes.create_string_buffer(struct.calcsize('!ii'))
        struct.pack_into('!ii', self.buf, 0, 0, self.data_block_num)
        self.f_handle.write(self.buf)
        self.f_handle.flush()

        # update data block head
        self.f_handle.seek(BLOCK_SIZE * last_Position[0])
        self.buf = ctypes.create_string_buffer(struct.calcsize('!ii'))
        struct.pack_into('!ii', self.buf, 0, last_Position[0], last_Position[1] + 1)
        self.f_handle.write(self.buf)
        self.f_handle.flush()

        # update data offset
        offset = struct.calcsize('!ii') + last_Position[1] * struct.calcsize('!i')
        beginIndex = BLOCK_SIZE - (last_Position[1] + 1) * record_len
        self.f_handle.seek(BLOCK_SIZE * last_Position[0] + offset)
        self.buf = ctypes.create_string_buffer(struct.calcsize('!i'))
        struct.pack_into('!i', self.buf, 0, beginIndex)
        self.f_handle.write(self.buf)
        self.f_handle.flush()

        # update data
        record_schema_address = struct.calcsize('!iii')
        update_time = '2016-11-16'  # update time
        self.f_handle.seek(BLOCK_SIZE * last_Position[0] + beginIndex)
        self.buf = ctypes.create_string_buffer(record_len)
        struct.pack_into('!ii10s', self.buf, 0, record_schema_address, record_content_len, update_time.encode('utf-8'))
        struct.pack_into('!' + str(record_content_len) + 's', self.buf, record_head_len, inputstr.encode('utf-8'))
        self.f_handle.write(self.buf.raw)
        self.f_handle.flush()

        return True

    # ------------------------------
    # show the data structure and its data
    # input:
    #       t
    # -------------------------------------

    def show_table_data(self):
        '''
        print('|    '.join(map(lambda x: x[0].decode('utf-8').strip(), self.field_name_list)))  # show the structure

        # the following is to show the data of the table
        for record in self.record_list:
            print(record)
        '''
        '''
        XXTong Edit 2025.05.25
        rewrite the show_table_data function to print the data in a formatted way
        '''
        print('|    '.join(field[0].decode('utf-8').strip() for field in self.field_name_list))

        for record in self.record_list:
            formatted_record = []
            for value, field in zip(record, self.field_name_list):
                if isinstance(value, bytes):
                    formatted_record.append(value.decode('utf-8').strip())
                elif field[1] == 2:  # integer
                    formatted_record.append(str(value))
                elif field[1] == 3:  # boolean
                    formatted_record.append(str(value))
                else:
                    formatted_record.append(str(value))
            print('|    '.join(formatted_record))
    # --------------------------------
    # to delete  the data file
    # input
    #       table name
    # output
    #       True or False
    # -----------------------------------
    def delete_table_data(self, tableName):

        # step 1: identify whether the file is still open
        if self.open == True:
            self.f_handle.close()
            self.open = False

        # step 2: remove the file from os   
        tableName.strip()
        if os.path.exists(tableName + '.dat'.encode('utf-8')):
            os.remove(tableName + '.dat'.encode('utf-8'))

        return True

    # ------------------------------
    # get the list of field information, each element of which is (field name, field type, field length)
    # input:
    #       
    # -------------------------------------

    def getFieldList(self):
        return self.field_name_list

    # ----------------------------------------
    # destructor
    # ------------------------------------------------
    def __del__(self):  # write the metahead information in head object to file

        if self.open == True:
            self.f_handle.seek(0)
            self.buf = ctypes.create_string_buffer(struct.calcsize('!ii'))
            struct.pack_into('!ii', self.buf, 0, 0, self.data_block_num)
            self.f_handle.write(self.buf)
            self.f_handle.flush()
            self.f_handle.close()
    


    def del_one_record(self, condition, field_name_list):
        """
        XXTong Edit 2025.05.25
        Delete a record from the table based on a condition.
        
        :param condition: A list containing [field_name, field_value] to identify the record to delete.
        :param field_name_list: List of all field names in the table.
        :return: True if deletion was successful, False otherwise.
        """
        field_index = field_name_list.index(condition[0])
        new_record_list = []
        deleted = False

        for record in self.record_list:
            record_value = record[field_index]
            if isinstance(record_value, bytes):
                record_value = record_value.decode('utf-8').strip()
            else:
                record_value = str(record_value).strip()

            condition_value = condition[1].strip()
            if condition_value.startswith("b'") and condition_value.endswith("'"):
                condition_value = condition_value[2:-1]  # Remove b'' if present
            if record_value != condition_value:
                new_record_list.append(record)
            else:
                deleted = True

        if deleted:
            self.record_list = new_record_list
            self._rewrite_data_file()
            return True
        return False

    def update_record(self, condition, new_value, field_name_list):
        """
        XXTong Edit 2025.05.25
        Update a record in the table based on a condition.
        
        :param condition: A list containing [field_name, old_value] to identify the record to update.
        :param new_value: A list containing [field_name, new_value] with the new value to set.
        :param field_name_list: List of all field names in the table.
        :return: True if update was successful, False otherwise.
        """
        try:
            condition_field_index = field_name_list.index(condition[0])
            update_field_index = field_name_list.index(new_value[0])
        except ValueError:
            print(f"错误：在表中未找到字段名。")
            return False

        updated = False

        for i, record in enumerate(self.record_list):
            record_value = record[condition_field_index]
            if isinstance(record_value, bytes):
                record_value = record_value.decode('utf-8').strip()
            else:
                record_value = str(record_value).strip()

            condition_value = condition[1].strip()
            if condition_value.startswith("b'") and condition_value.endswith("'"):
                condition_value = condition_value[2:-1]  # 移除 b'' 如果存在

            if record_value == condition_value:
                record_list = list(record)
                new_value_converted = self._convert_value(new_value[1], self.field_name_list[update_field_index][1])
                record_list[update_field_index] = new_value_converted
                self.record_list[i] = tuple(record_list)
                updated = True
                break

        if updated:
            self._rewrite_data_file()
            return True
        else:
            print(f"未找到匹配条件的记录：{condition[0]} = {condition[1]}")
            return False

    def _convert_value(self, value, field_type):
        """
        XXTong Edit 2025.05.25
        Convert a value to the appropriate type based on the field type.
        
        :param value: The value to convert.
        :param field_type: The type of the field (0: str, 1: varstr, 2: int, 3: bool).
        :return: The converted value.
        """
        if field_type == 0 or field_type == 1:
            return str(value)
        elif field_type == 2:
            return int(value)
        elif field_type == 3:
            return bool(value)
        else:
            return value

    def _rewrite_data_file(self):
        """
        XXTong Edit 2025.05.25
        Rewrite the entire data file with the updated record list.
        """
        self.f_handle.seek(0)
        self.f_handle.truncate()

        # Rewrite block 0 (meta information)
        self.dir_buf = ctypes.create_string_buffer(BLOCK_SIZE)
        struct.pack_into('!iii', self.dir_buf, 0, 0, len(self.record_list), self.num_of_fields)
        beginIndex = struct.calcsize('!iii')

        for field in self.field_name_list:
            struct.pack_into('!10sii', self.dir_buf, beginIndex, field[0], field[1], field[2])
            beginIndex += struct.calcsize('!10sii')

        self.f_handle.write(self.dir_buf)

        # Rewrite data blocks
        record_head_len = struct.calcsize('!ii10s')
        record_content_len = sum(map(lambda x: x[2], self.field_name_list))
        record_len = record_head_len + record_content_len
        MAX_RECORD_NUM = (BLOCK_SIZE - struct.calcsize('!ii')) // (record_len + struct.calcsize('!i'))

        current_block = 1
        records_in_block = 0
        for record in self.record_list:
            if records_in_block == 0:
                self.f_handle.seek(BLOCK_SIZE * current_block)
                block_header = struct.pack('!ii', current_block, min(MAX_RECORD_NUM, len(self.record_list) - (current_block - 1) * MAX_RECORD_NUM))
                self.f_handle.write(block_header)

            record_offset = BLOCK_SIZE - (records_in_block + 1) * record_len
            self.f_handle.seek(BLOCK_SIZE * current_block + struct.calcsize('!ii') + records_in_block * struct.calcsize('!i'))
            self.f_handle.write(struct.pack('!i', record_offset))

            record_data = struct.pack('!ii10s', struct.calcsize('!iii'), record_content_len, b'2023-05-24')
            for i, field in enumerate(self.field_name_list):
                value = record[i]
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                value = str(value).encode('utf-8')
                record_data += value.ljust(field[2])

            self.f_handle.seek(BLOCK_SIZE * current_block + record_offset)
            self.f_handle.write(record_data)

            records_in_block += 1
            if records_in_block == MAX_RECORD_NUM:
                current_block += 1
                records_in_block = 0

        self.f_handle.flush()

