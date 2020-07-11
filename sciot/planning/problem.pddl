
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
    (heater-on h01)
    (co2-crit c01)
    (shades-open s01)
    (light-crit l01)
)
        
(:goal
  (and
    (not (co2-crit c01) )
    (not (light-crit l01) )
    (not (temp-high ti01) )
    (not (temp-low ti01) )
  )
)

;;(:constraints
;;  (preference (always (forall (?h - heater) (not (heater-on ?h)))))
;;)


)

