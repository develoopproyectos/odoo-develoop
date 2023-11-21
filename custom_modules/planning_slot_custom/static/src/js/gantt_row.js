odoo.define('planning_slot_custom.gantt_row.js', function (require) {
    "use strict";

    var GanttRow = require('web_gantt.GanttRow');

    var GanttRowReturn = {
        start() {
            this._super.apply(this, arguments);
            
            var self = this;
            this.pills.forEach(function (pill) {
                console.log(pill);
                if (pill != null && pill != undefined && pill.x_expiration_date != false && pill.x_expiration_date != null && pill.x_expiration_date != undefined)
                {
                    var date_now = new Date();
                    date_now.setHours(0, 0, 0, 0);
                    const userTimezoneOffset = date_now.getTimezoneOffset() * 60000;
                    const d = new Date(date_now.getTime() - userTimezoneOffset);

                    var expiration_date = pill.x_expiration_date.toDate();
                    
                    if (expiration_date < d && pill.x_kanban_state != 'done' && pill.x_stage_id != undefined && 
                        (pill.x_stage_id[1].toLowerCase().includes("desarrollo") || pill.x_stage_id[1].toLowerCase().includes("planifica")))
                    {
                        var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                        if (row.length > 0)
                        {
                            row[0].className = row[0].className + " warning_red ";
                        }
                    }
                    else if (pill.color == "3") {
                        var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                        if (row.length > 0)
                        {
                            row[0].className = row[0].className + " warning_yellow ";
                        }                    
                    }
                    else if(pill.color == "10"){
                        var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                        if (row.length > 0)
                        {
                            row[0].className = row[0].className + " warning_green ";
                        }
                    }                  
                    else if(pill.color == "1" && (pill.x_stage_id[1].toLowerCase().includes("desarrollo") || pill.x_stage_id[1].toLowerCase().includes("planifica"))){
                        var row = self.$('.o_gantt_pill[data-id=' + pill.id + ']');
                        if (row.length > 0)
                        {
                            row[0].className = row[0].className + " warning_orange ";
                        }
                    }                  
                }
            });
        },
    };

    return GanttRow.include(GanttRowReturn);
});