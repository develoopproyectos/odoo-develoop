import csv
from odoo import api, models
import os
from odoo.modules.module import get_module_path
import re
import logging
_logger = logging.getLogger(__name__)

class PlanningImportTask(models.TransientModel):
    _name = 'planning.slot.import.task'

    @api.model
    def add_tasks_in_planning_from_csv(self, file_name):
        # Ruta del archivo CSV proporcionado como parámetro
        module_path = get_module_path('planning_slot_custom')        
        csv_file = os.path.join(module_path, 'data', file_name)
        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Obtener los valores de las columnas id y company_id de cada fila
                planning_id = row.get('planning_id')
                task_id = row.get('task_id')
                planning = self.env['planning.slot'].search([('id', '=', planning_id)], limit = 1)
                if not planning:
                    print(f"No se encontro con planning {planning_id}")
                    continue
                if not task_id:
                    continue 
                task = self.env['project.task'].search([('id', '=', task_id)], limit = 1)
                if task:
                    query = f"""UPDATE planning_slot SET task_id = '{task.id}' where id = {planning.id}"""
                    self._cr.execute(query)
                    self._cr.commit()
                    # print(f"se actualizo el planning {planning.id} con tarea {task_id}")
                else:
                    print(f"Planning encontrado {planning.id} SIN TAREA {task_id}")
                    

               


                
