#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include "sleepy.h"

int mysleep(long miliseconds)
{
   struct timespec req, rem;

   if(miliseconds > 999)
   {
        req.tv_sec = (int)(miliseconds / 1000);                            /* Must be Non-Negative */
        req.tv_nsec = (miliseconds - ((long)req.tv_sec * 1000)) * 1000000; /* Must be in range of 0 to 999999999 */
   }
   else
   {
        req.tv_sec = 0;                         /* Must be Non-Negative */
        req.tv_nsec = miliseconds * 1000000;    /* Must be in range of 0 to 999999999 */
   }
   return nanosleep(&req , &rem);
}
