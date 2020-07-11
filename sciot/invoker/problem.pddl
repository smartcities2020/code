(define (problem myproblem)
  (:domain iotcrap)
(:objects 
   w01 - window
   s01 - shades
   h01 - heater
   a01 - alexa
   c01 - co2
   m01 - hum
  ti01 - inside       
  to01 - outside
   l01 - light
)


(:init
 (not (co2-crit c01)      )  

 (not (temp-high ti01)    )  
 (not (temp-low ti01)     )  
 (not (temp-high to01)    )  
 (not (temp-low to01)     )  

 (not (hum-high m01)      )  
 (not (hum-low m01)       )  

 (not (light-crit l01)    )  

   (window-closed w01) 
       (shades-up s01)     
 (not (heater-on h01)     )  
)



(:goal

  (and
    (not (co2-crit c01) )
    (not (light-crit l01) )
    (not (temp-high ti01) )
    (not (temp-low ti01) )








 	(not (heater-on h01) ) 


  )

)
)
