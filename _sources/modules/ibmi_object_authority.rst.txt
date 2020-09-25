
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_object_authority.py

.. _ibmi_object_authority_module:


ibmi_object_authority -- Grant, revoke or display object authority
==================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_object_authority`` module can do the named object(s) authority management(grant, revoke and display).





Parameters
----------


     
asp_device
  Specifies the auxiliary storage pool (ASP) device name where the library that contains the object (OBJ parameter) is located.

  The ASP group name is the name of the primary ASP device within the ASP group.

  Valid for all the operations, but operations display will igonre this option.


  | **required**: false
  | **type**: str
  | **default**: \*


     
asp_group
  Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread. The ASP group name is the name of the primary ASP device within the ASP group. The different for asp_group and asp_device or ref_asp_device are, the asp_group make the current ansible thread run under the asp_group. the asp_device or ref_asp_device is the search scope for the object. If you want to searh the object or ref_object in an ASP, the asp_group must be set and varied on, asp_device or ref_asp_device can be set as ``*`` for searching in the ASP and also the system ASP or asp_group name to just search in this ASP.

  Valid for all the operations


  | **required**: false
  | **type**: str
  | **default**: \*SYSBAS


     
authority
  Specifies the authority to be granted or revoked to the users specified for the Users (USER) parameter.

  Valid only for operations grant and revoke.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: ['\*CHANGE']
  | **choices**: \*CHANGE, \*ALL, \*USE, \*EXCLUDE, \*AUTL, \*OBJALTER, \*OBJEXIST, \*OBJMGT, \*OBJOPR, \*OBJREF, \*ADD, \*DLT, \*READ, \*UPD, \*EXECUTE


     
authorization_list
  Specifies the authorization list that is to grant or revok on the object, only vaild for operation grant_autl or revoke_autl.

  Valid only for operations grant_autl and revoke_autl, you must specify a value other than ``''``.


  | **required**: false
  | **type**: str


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
object_library
  Specify the name of the library to be searched.

  Valid for all the operations.

  When operation is display, special value as ``*LIBL``, ``*CURLIB``, ``*ALL``, ``*ALLUSR``, ``*USRLIBL``, ``*ALLAVL``, ``*ALLUSRAVL`` are not supported.


  | **required**: false
  | **type**: str
  | **default**: \*LIBL


     
object_name
  Specify the name of the object for which specific authority is to be granted, revoked or displayed to one or more users.

  Valid for all the operations.


  | **required**: True
  | **type**: str


     
object_type
  Specify the object type of the object for which specific authorities are to be granted, revoked or displayed to the specified users.

  Supported object type refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm

  Valid for all the operations.


  | **required**: True
  | **type**: str
  | **choices**: \*ALL, \*ALRTBL, \*BNDDIR, \*CFGL, \*CHTFMT, \*CLD, \*CLS, \*CMD, \*CNNL, \*COSD, \*CRG, \*CRQD, \*CSI, \*CSPMAP, \*CSPTBL, \*CTLD, \*DEVD, \*DTAARA, \*DTADCT, \*DTAQ, \*EDTD, \*FCT, \*FILE, \*FNTRSC, \*FNTTBL, \*FORMDF, \*FTR, \*GSS, \*IGCDCT, \*IGCSRT, \*IGCTBL, \*IMGCLG, \*IPXD, \*JOBD, \*JOBQ, \*JOBSCD, \*JRN, \*JRNRCV, \*LIB, \*LIND, \*LOCALE, \*M36, \*M36CFG, \*MEDDFN, \*MENU, \*MGTCOL, \*MODD, \*MODULE, \*MSGF, \*MSGQ, \*NODGRP, \*NODL, \*NTBD, \*NWID, \*NWSCFG, \*NWSD, \*OUTQ, \*OVL, \*PAGDFN, \*PAGSEG, \*PDFMAP, \*PDG, \*PGM, \*PNLGRP, \*PRDAVL, \*PRDDFN, \*PRDLOD, \*PSFCFG, \*QMFORM, \*QMQRY, \*QRYDFN, \*RCT, \*S36, \*SBSD, \*SCHIDX, \*SPADCT, \*SQLPKG, \*SQLUDT, \*SQLXSR, \*SRVPGM, \*SSND, \*SVRSTG, \*TBL, \*TIMZON, \*USRIDX, \*USRPRF, \*USRQ, \*USRSPC, \*VLDL, \*WSCST


     
operation
  The authority operation.

  Valid for all the operations.

  Operation grant is to grant user(s) authority(s) to object(s).

  Operation revoke is to revoke user(s) authority(s) from object(s).

  Operation display is to display object(s)'s authority information.

  Operation grant_autl is to grant a authorization list(the authorization list object contains the list of authority) to object(s).

  Operation revoke_autl is to revoke authorization list from object(s).

  Operation grant_ref is to grant the reference object to be queried to obtain authorization information.

  For more information about reference object, refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm


  | **required**: True
  | **type**: str
  | **choices**: grant, revoke, display, grant_autl, revoke_autl, grant_ref


     
ref_asp_device
  Specifies the auxiliary storage pool (ASP) device name where the library that contains the reference object is located.

  The ASP group name is the name of the primary ASP device within the ASP group.

  Valid only for operation grant_ref


  | **required**: false
  | **type**: str
  | **default**: \*


     
ref_object_library
  Specify the name of the library to be searched.

  Valid only for operation grant_ref.


  | **required**: false
  | **type**: str
  | **default**: \*LIBL


     
ref_object_name
  Specify the name of the reference object for which specific authority is to be granted, revoked or displayed to one or more users.

  Valid only for operation grant_ref, you must specify a value other than ``''``.


  | **required**: false
  | **type**: str


     
ref_object_type
  Specify the reference object type of the object for which specific authorities are to be granted, revoked or displayed to the specified users.

  Supported reference object type refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm

  Valid only for operation grant_ref.


  | **required**: false
  | **type**: str
  | **default**: \*OBJTYPE
  | **choices**: \*OBJTYPE, \*ALRTBL, \*AUTL, \*BNDDIR, \*CFGL, \*CHTFMT, \*CLD, \*CLS, \*CMD, \*CNNL, \*COSD, \*CRG, \*CRQD, \*CSI, \*CSPMAP, \*CSPTBL, \*CTLD, \*DEVD, \*DTAARA, \*DTADCT, \*DTAQ, \*EDTD, \*FCT, \*FILE, \*FNTRSC, \*FNTTBL, \*FORMDF, \*FTR, \*GSS, \*IGCDCT, \*IGCSRT, \*IGCTBL, \*IMGCLG, \*IPXD, \*JOBD, \*JOBQ, \*JOBSCD, \*JRN, \*JRNRCV, \*LIB, \*LIND, \*LOCALE, \*M36, \*M36CFG, \*MEDDFN, \*MENU, \*MGTCOL, \*MODD, \*MODULE, \*MSGF, \*MSGQ, \*NODGRP, \*NODL, \*NTBD, \*NWID, \*NWSCFG, \*NWSD, \*OUTQ, \*OVL, \*PAGDFN, \*PAGSEG, \*PDFMAP, \*PDG, \*PGM, \*PNLGRP, \*PRDDFN, \*PRDLOD, \*PSFCFG, \*QMFORM, \*QMQRY, \*QRYDFN, \*RCT, \*S36, \*SBSD, \*SCHIDX, \*SPADCT, \*SQLPKG, \*SQLUDT, \*SQLXSR, \*SRVPGM, \*SSND, \*SVRSTG, \*TBL, \*TIMZON, \*USRIDX, \*USRPRF, \*USRQ, \*USRSPC, \*VLDL, \*WSCST


     
replace_authority
  Specifies whether the authorities replace the user's current authorities.

  Valid only for operations grant.


  | **required**: false
  | **type**: bool


     
user
  Specifies one or more users to whom authority for the named object is to be granted or revoked.

  Valid only for operations grant and revoke.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: ['']




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Grant 1 user 1 authority on object
     ibmi_object_authority:
       operation: grant
       object_name: testobj
       object_library: testlib
       object_type: '*DTAARA'
       user: testuser
       authority: '*ALL'

   - name: Revoke 1 user's 2 authorities on object
     ibmi_object_authority:
       operation: 'revoke'
       object_name: 'ANSIBLE'
       object_library: 'CHANGLE'
       user:
         - 'CHANGLE'
       authority:
         - '*READ'
         - '*DLT'

   - name: Display the authority
     ibmi_object_authority:
       operation: display
       object_name: testobj
       object_library: testlib
       object_type: '*DTAARA'

   - name: Grant the reference object authority
     ibmi_object_authority:
       operation: grant_ref
       object_name: testobj
       object_library: testlib
       object_type: '*DTAARA'
       ref_object: testrefobj
       ref_object_library: testreflib
       ref_object_type: '*DTAARA'

   - name: Revoke the authority list on object
     ibmi_object_authority:
       operation: revoke_autl
       object_name: testobj
       object_library: testlib
       object_type: '*DTAARA'
       authorization_list: 'MYAUTL'

   - name: grant user 2 authority on an iasp
     ibmi_object_authority:
       operation: 'grant'
       object_name: 'iasp1'
       object_library: 'CHANGLE2'
       object_type: '*DTAARA'
       asp_group: 'IASP1'
       user:
         - 'CHANGLE'
       authority:
         - '*READ'
         - '*DLT'






See Also
--------

.. seealso::

   - :ref:`ibmi_object_find_module`



Return Values
-------------


   
                              
       stdout
        | The standard output
      
        | **returned**: when rc as 0(success) and the operation is not display
        | **type**: str
        | **sample**: CPI2204: Authority given to 1 objects. Not given to 0 objects. Partially given to 0 objects.

            
      
      
                              
       stderr
        | The standard error
      
        | **returned**: when rc as no-zero(failure)
        | **type**: str
        | **sample**: CPF2209: Library CHANGL not found

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The command standard output split in lines
      
        | **returned**: when rc as 0(success) and the operation is not display
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPI2204: Authority given to 1 objects. Not given to 0 objects. Partially given to 0 objects.", "CPC2201: Object authority granted."]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines
      
        | **returned**: when rc as no-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2209: Library CHANGL not found"]
            
      
      
                              
       object_authority_list
        | The result set of object authority list
      
        | **returned**: When rc as 0(success) and operation is display
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"AUTHORIZATION_LIST": "", "AUTHORIZATION_NAME": "*PUBLIC", "DATA_ADD": "YES", "DATA_DELETE": "YES", "DATA_EXECUTE": "YES", "DATA_READ": "YES", "DATA_UPDATE": "YES", "OBJECT_ALTER": "NO", "OBJECT_AUTHORITY": "*CHANGE", "OBJECT_EXISTENCE": "NO", "OBJECT_MANAGEMENT": "NO", "OBJECT_NAME": "ANSIBLE", "OBJECT_OPERATIONAL": "YES", "OBJECT_REFERENCE": "NO", "OBJECT_SCHEMA": "CHANGLE", "OBJECT_TYPE": "*DTAARA", "OWNER": "CHANGLE", "SQL_OBJECT_TYPE": "", "SYSTEM_OBJECT_NAME": "ANSIBLE", "SYSTEM_OBJECT_SCHEMA": "CHANGLE", "TEXT_DESCRIPTION": ""}]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
