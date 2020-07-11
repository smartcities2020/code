
(define (domain iotcrap)

(:types
        window shades heater alexa co2 hum temp light - object
        inside outside - temp        ;; internal and external temperature
    )

;; the temperature high/low predicates indicate that the selected temperature is outside of the the given bounds, either too warm or too cold
    (:predicates
        (window-closed ?w - window)
        (shades-up ?ws - shades)
        (heater-on ?h - heater)
        (co2-crit ?c - co2)
        (temp-high ?t - temp)
        (temp-low ?t - temp)
        (hum-high ?m - hum)
        (hum-low ?m - hum)
        (light-crit ?l - light)
        ;; user requested versions
	;; - tbd? -

    )
;; the window must not open when we couls dave energy, except co2 is too high    
 (:action a-window-open
   :parameters (?w - window ?c - co2 ?h - heater ?i - inside ?o - outside)
   :precondition 
       (and 
           (window-closed ?w) 
           (not (heater-on ?h))  
           (or               
                (co2-crit ?c)    
                (and 
                    (temp-high ?i)  
                    (not (temp-high ?o))
                )
                (and 
                    (temp-low ?i)  
                    (not (temp-low ?o))
                )
           )
       )
   :effect 
       (and
           (not (window-closed ?w)) 
           (not(co2-crit ?c)) 
           (not (temp-high ?i))
           (not (temp-low ?i))
       )
 )
 
(:action a-window-close
   :parameters (?w - window ?c - co2 ?h - heater ?i - inside ?o - outside)
   :precondition (and
	(not (window-closed ?w) )
        (not 
        	(or               
        	     (co2-crit ?c)    
        	     (and 
        	         (temp-high ?i)  
        	         (not (temp-high ?o))
        	     )
        	     (and 
        	         (temp-low ?i)  
        	         (not (temp-low ?o))
        	     )
        	)
	)           
	) 
   :effect (window-closed ?w)
 )
 
;; the heater can turn of at any time 
(:action a-heater-off
    :parameters (?h - heater ?i - inside ?o - outside ?w - window )
    :precondition (and
          (heater-on ?h)
          (or
            (not (temp-low ?o) )
            (not (temp-low ?i) )
        )
     )
    :effect (not (heater-on ?h) )
     
)

;; the heater must not turn on when we could save energy (window is open or outside is warm)
(:action a-heater-on
    :parameters (?h - heater ?i - inside ?o - outside ?w - window )
    :precondition 
    (and
        (temp-low ?i)
        (temp-low ?o)
        (not (heater-on ?h) )
        (window-closed ?w)
    )
    :effect (and
        (heater-on ?h)
        (not (temp-low ?i) )    
    )
)

(:action a-shades-down
    :parameters (?s - shades ?l - light)
    :precondition
    (and 
        (shades-up ?s)
        (light-crit ?l))
    :effect
    (and
        (not (shades-up ?s)) 
        (not (light-crit ?l))
    )
)
    
(:action a-shades-up
    :parameters (?s - shades ?l - light )
    :precondition (and
	(not (shades-up ?s))
	(not (light-crit ?l))
	)
    :effect (shades-up ?s)
)



)
