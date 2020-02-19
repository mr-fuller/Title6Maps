with luc_woo as(
select *
from title6_b_2017
where "GEO_ID" like '%39095%' or "GEO_ID" like '%39173%'
	)
select sum(luc_woo."B01001_001E") 
from luc_woo
where luc_woo_ej in ('both','poc','low_income');