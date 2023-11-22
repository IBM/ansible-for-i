#include <stdio.h>                    // printf and strlen
#include <except.h>                   // exception handler
#include <qusec.h>                    // Qus_EC_t
#include <qmhsndpm.h>                 // QMHSNDPM

int sendMsg(char *pMsgData)
{
    char MSGKey[4];
	Qus_EC_t errorCode;
    memset(&errorCode, 0, sizeof(errorCode));
	errorCode.Bytes_Provided = sizeof(errorCode);
	#pragma exception_handler(unexpected, 0, _C1_ALL, _C2_ALL, _CTLA_HANDLE)	
    QMHSNDPM("CPF9897"                 // Message identifier
	        , "QCPFMSG   *LIBL     "   // Qualified message file name
	        , pMsgData                 // Replacement data
	        , strlen(pMsgData)         // Length of replacement data
	        , "*INFO     "             // message type
	        ,  "*PGMBDY   "            // call stack entry to send the message
	        , 1                        // message queue number
            , MSGKey                   // message key
            , &errorCode               // Error code feedback
	       );
    #pragma disable_handler
    if (errorCode.Bytes_Available)
	{
		printf("sendMsg() - QMHSNDPM API return error='%0.7s'", errorCode.Exception_Id);
        return 1;
	}
    
    if (0)
    {
        unexpected:
        printf("sendMsg() - unexpected exception occurred during call QMHSNDPM API");
        return 1;
    }     	
    
    return 0;
}

int main()
{
    int rc = sendMsg("Hello world!");
    return 0;
}
