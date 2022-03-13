/* Passord er SHA-512 hash*/
INSERT INTO bruker VALUES(
    "norasophie96@hotmail.com", 
    "$6$Bw8.EDGU9rjSY.av$2jHOnnI7zrcm/iweDJgI7wwQzSLqXxtiyzqBSHP7bux9W3p3DH.i41n2NK2KOcaNoCM87AbAgYPrWb277Xsza0", 
    "Nora Sophie", "Backe"); 
    /* Passord: Passord1 */


INSERT INTO bruker VALUES(
    "hevos@hvcn.com", 
    "$6$bR5L1BEKew0X1Sd$mjuHPtiPI2PMEenS8xqxTp5oD0CW6oARAyutAquk7kh9T4uLcZPnN58LWcy8epwTpBV.CrlEDBxDgtYz3LdtT/", 
    "Håkon Vestreng", "Solberg"); 
    /* Passord: Passord2 */


INSERT INTO bruker VALUES(
    "viktor@hvcn.com", 
    "$6$JK8Uo.7Yk7F$2FRH8QFChm7asypxzJeExTffvEqZ98jxRR98QzVMAPaYvRciUg6aVcSUJqDLjne/7hhhTMghAAp0WDsDnY.6u/", 
    "Viktor Ormestad", "Larsen"); 
    /* Passord: Passord3 */


INSERT INTO bruker VALUES(
    "chris@hvcn.com", 
    "$6$agON901/B3SJ$R0hMcr34oi30G9jj.pNq61ZepXFJhVm0Qjkmkk1/mjKi6ccibRTyJMBZCxKM86pAmbgVLaG8HEn2Zt1oU.ZyB0", 
    "Christian Andre Waldum", 
    "Thorsø"); 
    /* Passord: Passord4 */


INSERT INTO sesjon VALUES(1534, "norasophie96@hotmail.com");
INSERT INTO sesjon VALUES(2324, "hevos@hvcn.com");
INSERT INTO sesjon VALUES(3356, "viktor@hvcn.com");
INSERT INTO sesjon VALUES(4423, "chris@hvcn.com");


INSERT INTO dikt VALUES(1, "Dette er et hyggelig dikt", "norasophie96@hotmail.com");
INSERT INTO dikt VALUES(2, "Dette er et sint dikt", "chris@hvcn.com");
INSERT INTO dikt VALUES(3, "Dette er et glad dikt", "norasophie96@hotmail.com");
INSERT INTO dikt VALUES(4, "Dette er et trist dikt", "viktor@hvcn.com");
INSERT INTO dikt VALUES(5, "Dette er et slemt dikt", "hevos@hvcn.com");