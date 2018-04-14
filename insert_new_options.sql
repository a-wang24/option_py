update option_last ol 
    set (tradedate,volumn,last,change,bid,ask,openinterest) = (select tradedate,volumn,last,change,bid,ask,openinterest from optionx  where optionsymbol=ol.optionsymbol)
WHERE EXISTS (select tradedate,volumn,last,change,bid,ask,openinterest from optionx where optionsymbol=ol.optionsymbol and (volumn <> ol.volumn or last <> ol.last));

commit;

insert into option_last
select * from optionx where optionsymbol not in (select optionsymbol from option_last);

commit;

insert into optionquotes
select * from option_last where tradedate=trunc(sysdate);
commit;

truncate table optionx;
    

