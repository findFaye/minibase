
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'statementCOMMA CONSTANT CREATE DELETE DROP EQX FROM INSERT INTO LPAREN RPAREN SELECT SET STAR TABLE TCNAME TYPE UPDATE VALUES WHEREstatement : query\n                 | create_table\n                 | insert_stmt\n                 | delete_stmt\n                 | update_stmt\n                 | drop_tablecreate_table : CREATE TABLE TCNAME LPAREN field_defs RPARENfield_defs : field_def\n                  | field_def COMMA field_defsfield_def : TCNAME TYPEinsert_stmt : INSERT INTO TCNAME VALUES LPAREN value_list RPARENvalue_list : CONSTANT\n                  | CONSTANT COMMA value_listdelete_stmt : DELETE FROM TCNAMEupdate_stmt : UPDATE TCNAME SET TCNAME EQX CONSTANT WHERE TCNAME EQX CONSTANTdrop_table : DROP TABLE TCNAMEquery : SELECT sel_list FROM table_name opt_wheresel_list : STARsel_list : TCNAME rest_fieldsrest_fields : COMMA TCNAME rest_fields\n                   | table_name : TCNAMEopt_where : WHERE condition\n                 | condition : TCNAME EQX CONSTANT'
    
_lr_action_items = {'SELECT':([0,],[8,]),'CREATE':([0,],[9,]),'INSERT':([0,],[10,]),'DELETE':([0,],[11,]),'UPDATE':([0,],[12,]),'DROP':([0,],[13,]),'$end':([1,2,3,4,5,6,7,27,29,30,31,36,44,47,54,57,61,],[0,-1,-2,-3,-4,-5,-6,-14,-16,-24,-22,-17,-23,-7,-11,-25,-15,]),'STAR':([8,],[15,]),'TCNAME':([8,12,17,18,19,21,22,24,28,33,37,48,56,],[16,20,25,26,27,29,31,32,35,39,45,39,59,]),'TABLE':([9,13,],[17,21,]),'INTO':([10,],[18,]),'FROM':([11,14,15,16,23,32,38,],[19,22,-18,-21,-19,-21,-20,]),'COMMA':([16,32,41,46,50,],[24,24,48,-10,55,]),'SET':([20,],[28,]),'LPAREN':([25,34,],[33,42,]),'VALUES':([26,],[34,]),'WHERE':([30,31,51,],[37,-22,56,]),'EQX':([35,45,59,],[43,52,60,]),'TYPE':([39,],[46,]),'RPAREN':([40,41,46,49,50,53,58,],[47,-8,-10,54,-12,-9,-13,]),'CONSTANT':([42,43,52,55,60,],[50,51,57,50,61,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement':([0,],[1,]),'query':([0,],[2,]),'create_table':([0,],[3,]),'insert_stmt':([0,],[4,]),'delete_stmt':([0,],[5,]),'update_stmt':([0,],[6,]),'drop_table':([0,],[7,]),'sel_list':([8,],[14,]),'rest_fields':([16,32,],[23,38,]),'table_name':([22,],[30,]),'opt_where':([30,],[36,]),'field_defs':([33,48,],[40,53,]),'field_def':([33,48,],[41,41,]),'condition':([37,],[44,]),'value_list':([42,55,],[49,58,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> query','statement',1,'p_statement','parser_db.py',7),
  ('statement -> create_table','statement',1,'p_statement','parser_db.py',8),
  ('statement -> insert_stmt','statement',1,'p_statement','parser_db.py',9),
  ('statement -> delete_stmt','statement',1,'p_statement','parser_db.py',10),
  ('statement -> update_stmt','statement',1,'p_statement','parser_db.py',11),
  ('statement -> drop_table','statement',1,'p_statement','parser_db.py',12),
  ('create_table -> CREATE TABLE TCNAME LPAREN field_defs RPAREN','create_table',6,'p_create_table','parser_db.py',16),
  ('field_defs -> field_def','field_defs',1,'p_field_defs','parser_db.py',20),
  ('field_defs -> field_def COMMA field_defs','field_defs',3,'p_field_defs','parser_db.py',21),
  ('field_def -> TCNAME TYPE','field_def',2,'p_field_def','parser_db.py',29),
  ('insert_stmt -> INSERT INTO TCNAME VALUES LPAREN value_list RPAREN','insert_stmt',7,'p_insert_stmt','parser_db.py',33),
  ('value_list -> CONSTANT','value_list',1,'p_value_list','parser_db.py',37),
  ('value_list -> CONSTANT COMMA value_list','value_list',3,'p_value_list','parser_db.py',38),
  ('delete_stmt -> DELETE FROM TCNAME','delete_stmt',3,'p_delete_stmt','parser_db.py',45),
  ('update_stmt -> UPDATE TCNAME SET TCNAME EQX CONSTANT WHERE TCNAME EQX CONSTANT','update_stmt',10,'p_update_stmt','parser_db.py',49),
  ('drop_table -> DROP TABLE TCNAME','drop_table',3,'p_drop_table','parser_db.py',55),
  ('query -> SELECT sel_list FROM table_name opt_where','query',5,'p_query_sfw','parser_db.py',59),
  ('sel_list -> STAR','sel_list',1,'p_sel_list_star','parser_db.py',66),
  ('sel_list -> TCNAME rest_fields','sel_list',2,'p_sel_list_names','parser_db.py',70),
  ('rest_fields -> COMMA TCNAME rest_fields','rest_fields',3,'p_rest_fields','parser_db.py',75),
  ('rest_fields -> <empty>','rest_fields',0,'p_rest_fields','parser_db.py',76),
  ('table_name -> TCNAME','table_name',1,'p_table_name','parser_db.py',83),
  ('opt_where -> WHERE condition','opt_where',2,'p_opt_where','parser_db.py',87),
  ('opt_where -> <empty>','opt_where',0,'p_opt_where','parser_db.py',88),
  ('condition -> TCNAME EQX CONSTANT','condition',3,'p_condition','parser_db.py',95),
]
