odoo.define('planning_slot_custom.gantt_row.js', function (require) {
    "use strict";

    var GanttRow = require('web_gantt.GanttRow');

    var GanttRowReturn = {
        template: 'CustomGanttView.Row',
        start() {
            this._super.apply(this, arguments);
            
            var self = this;
            this.pills.forEach(function (pill) {                
                // Asignar nuevo texto a las Pill con horas asiganadas y el nombre de la tarea
                let cell = self.$('.o_gantt_pill[data-id=' + pill.id + '] .o_gantt_pill_title');
                if (cell.length > 0)
                    {
                        let hours = Math.floor(pill.allocated_hours);
                        let minutes = Math.round((pill.allocated_hours - hours) * 60);
                        cell.text('('+hours+'h'+(minutes < 10 ? "0" : "")+ minutes +') - '+ pill.display_name) 
                    }
                
                if(pill.aggregatedPills){                
                    var row = self.$('div[title="' + pill.display_name + '"]').parent();                    
                    /* const regex = /(\d+):(\d+)Hrs/;
                    const match = (pill.display_name).match(regex); */
                    const total_hours = (pill.display_name).split(' - ');
                    const [hora, minutos] = total_hours[1].replace("Hrs", "").split(":");
                    if (!pill.is_total) {
                        const hora_int = parseInt(hora,10)
                        const minutos_int = parseInt(minutos,10)
                        const hours = hora_int + (minutos_int / 60);                     
                        if(pill.aggregatedPills[0].x_resourse_plannable_hours && hours > pill.aggregatedPills[0].x_resourse_plannable_hours)
                        {
                            if(row.length > 0)
                                row[0].className = row[0].className + " warning_red ";
                        }
                    }
                }
                
                if (pill != null && pill != undefined)
                {
                    var date_now = new Date();
                    date_now.setHours(0, 0, 0, 0);
                    const userTimezoneOffset = date_now.getTimezoneOffset() * 60000;
                    const d = new Date(date_now.getTime() - userTimezoneOffset);
                    let is_red = false;
                    if(pill.planned_date_end != false && pill.planned_date_end != null && pill.planned_date_end != undefined){
                        
                        
                        var expiration_date = pill.planned_date_end.toDate();
                        
                        if (expiration_date < d && pill.x_kanban_state != 'done' && pill.x_stage_id != undefined && 
                        (pill.x_stage_id[1].toLowerCase().includes("desarrollo") || pill.x_stage_id[1].toLowerCase().includes("planifica")))
                        {
                            var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                            if (row.length > 0)
                            {
                                row[0].className = row[0].className + " warning_red ";
                                is_red = true
                            }
                        }
                    }
                    if (pill.color == "3" && is_red == false ) {
                        
                        var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                        if (row.length > 0)
                        {
                            row[0].className = row[0].className + " warning_yellow ";
                        }                    
                    }
                    else if(pill.color == "10" && is_red == false){
                        
                        var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                        if (row.length > 0)
                        {
                            row[0].className = row[0].className + " warning_green ";
                        }
                    }                  
                    else if(pill.color == "1" && (pill.x_stage_id[1].toLowerCase().includes("desarrollo") || pill.x_stage_id[1].toLowerCase().includes("planifica"))&& is_red == false){
                        
                        var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                        if (row.length > 0)
                        {
                            row[0].className = row[0].className + " warning_orange ";
                        }
                    }                  
                }
                
            });
        },
        _aggregateGroupedPills: function () {            
            var self = this;
            var sortedPills = _.sortBy(_.map(this.pills, _.clone), 'startDate');
            var firstPill = sortedPills[0];
            firstPill.count = 1;

            var timeToken = this.SCALES[this.state.scale].time;
            var precision = this.viewInfo.activeScaleInfo.precision;
            var cellTime = this.SCALES[this.state.scale].cellPrecisions[precision];
            var intervals = _.reduce(this.viewInfo.slots, function (intervals, slotStart) {
                intervals.push(slotStart);
                if (precision === 'half') {
                    intervals.push(slotStart.clone().add(cellTime, timeToken));
                }
                return intervals;
            }, []);

            this.pills = _.reduce(intervals, function (pills, intervalStart) {
                var intervalStop = intervalStart.clone().add(cellTime, timeToken);
                var pillsInThisInterval = _.filter(self.pills, function (pill) {
                    return pill.startDate < intervalStop && pill.stopDate > intervalStart;
                });
                if (pillsInThisInterval.length) {
                    var previousPill = pills[pills.length - 1];
                    var isContinuous = previousPill &&
                        _.intersection(previousPill.aggregatedPills, pillsInThisInterval).length;
                    if (isContinuous && previousPill.count === pillsInThisInterval.length) {
                            // Enlarge previous pill so that it spans the current slot
                            previousPill.stopDate = intervalStop;
                            // previousPill.aggregatedPills = previousPill.aggregatedPills.concat(pillsInThisInterval);
                    } 
                    var newPill = {
                        is_total: self.name == 'Total'? true: false,
                        id: 0,
                        count: pillsInThisInterval.length,
                        aggregatedPills: pillsInThisInterval,
                        startDate: moment.max(_.min(pillsInThisInterval, 'startDate').startDate, intervalStart),
                        stopDate: moment.min(_.max(pillsInThisInterval, 'stopDate').stopDate, intervalStop),
                    };

                        // Enrich the aggregates with consolidation data
                    if (self.consolidate && self.consolidationParams.field) {
                        newPill.consolidationValue = pillsInThisInterval.reduce(
                            function (sum, pill) {
                                if (!pill[self.consolidationParams.excludeField]) {
                                    return sum + pill[self.consolidationParams.field];
                                }
                                return sum; // Don't sum this pill if it is excluded
                            },
                            0
                        );
                        newPill.consolidationMaxValue = self.consolidationParams.maxValue;
                        newPill.consolidationExceeded = newPill.consolidationValue > newPill.consolidationMaxValue;
                    }

                    pills.push(newPill);
                    
                    // if (isContinuous && previousPill.count === pillsInThisInterval.length) {
                    //     // Enlarge previous pill so that it spans the current slot
                    //     // previousPill.stopDate = intervalStop;
                    //     // previousPill.aggregatedPills = previousPill.aggregatedPills.concat(pillsInThisInterval);
                    // } else {
                    //     var newPill = {
                    //         id: 0,
                    //         count: pillsInThisInterval.length,
                    //         aggregatedPills: pillsInThisInterval,
                    //         startDate: moment.max(_.min(pillsInThisInterval, 'startDate').startDate, intervalStart),
                    //         stopDate: moment.min(_.max(pillsInThisInterval, 'stopDate').stopDate, intervalStop),
                    //     };

                    //     // Enrich the aggregates with consolidation data
                    //     if (self.consolidate && self.consolidationParams.field) {
                    //         newPill.consolidationValue = pillsInThisInterval.reduce(
                    //             function (sum, pill) {
                    //                 if (!pill[self.consolidationParams.excludeField]) {
                    //                     return sum + pill[self.consolidationParams.field];
                    //                 }
                    //                 return sum; // Don't sum this pill if it is excluded
                    //             },
                    //             0
                    //         );
                    //         newPill.consolidationMaxValue = self.consolidationParams.maxValue;
                    //         newPill.consolidationExceeded = newPill.consolidationValue > newPill.consolidationMaxValue;
                    //     }

                    //     pills.push(newPill);
                    // }
                }
                return pills;
            }, []);
            var maxCount = _.max(this.pills, function (pill) {
                return pill.count;
            }).count;
            var minColor = 215;
            var maxColor = 100;
            this.pills.forEach(function (pill) {
                pill.consolidated = true;
                if (self.consolidate && self.consolidationParams.maxValue) {
                    pill.status = pill.consolidationExceeded ? 'danger' : 'success';
                    pill.display_name = pill.consolidationValue;
                } else {
                    var color = minColor - ((pill.count - 1) / maxCount) * (minColor - maxColor);
                    pill.style = _.str.sprintf("background-color: rgba(%s, %s, %s, 0.6)", color, color, color);
                    pill.display_name = pill.count;
                }
            });
            this.pills.forEach(function (pill) {
                pill.consolidated = true;
                if (self.consolidate && self.consolidationParams.maxValue) {
                    
                } else {
                    var total_hours  = 0
                    pill.aggregatedPills.forEach(function (agPill){
                        let start_date = agPill.start_datetime
                        let end_date = agPill.end_datetime
                        let difference_ms = end_date - start_date;
                        let difference_days = Math.ceil(difference_ms / (1000 * 60 * 60 * 24));
                        if (difference_days > 1) {
                            total_hours += (agPill.allocated_hours/(difference_days));
                        } else {
                            total_hours += agPill.allocated_hours;
                        }

                    })
                    let hours = Math.floor(total_hours);
                    let minutes = Math.round((total_hours - hours) * 60);
                    pill.display_name = pill.display_name + ' - '+ hours + ":" + (minutes < 10 ? "0" : "") + minutes + 'Hrs';
                }
                
            });        
        },
    };

    return GanttRow.include(GanttRowReturn);
});