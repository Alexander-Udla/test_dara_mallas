from odoo import fields, models,api
import openpyxl
from openpyxl.styles import PatternFill
from io import BytesIO
import base64
from datetime import date, datetime
class stop_sp_homologations(models.Model):
    _name="dara_mallas.stop_sp_homologations"
    file=fields.Binary("Reporte")
    file_name=fields.Char("Reporte de cambios en malla congelada")

    def find_mirror_changed_rules_periods(self):
        mirrors = self.env['dara_mallas.subject_rule_mirror'].search([])

        # con mapped buscamos los atributos relacionados
        result = mirrors.mapped(lambda r: {
            'rule': r.subject_id.code,
            'period': r.period_id.name,
            'area': r.area_id.code
        })

        distinct_result = []
        for res in result:
            if res not in distinct_result:
                distinct_result.append(res)

        return distinct_result

    def find_original_changed_rules(self, area, period, rule):
        period_str = str(period) if period != 0 else '000000'

        subject_rules = self.env['dara_mallas.subject_rule'].search([
            ('area_id.code', '=', area),
            ('period_id.name', '=', period_str),
            ('subject_id.code', '=', rule)
        ])

        result = []

        for sr in subject_rules:
            homologation = sr.subject_homologation_ids
            for h in homologation:
                result.append({
                    'period': period_str,
                    'area': sr.area_id.code,
                    'rule': sr.subject_id.code,
                    'condition': h.condition,
                    'conector': h.group_id.name,
                    'subject': h.homologation_subject_id.code,
                    'prueba': h.test if h.test != '0' else None,
                    'test puntaje minimo': h.min_score if h.test != '0' else None,
                    'test puntaje maximo': h.max_score if h.test != '0' else None,
                    'rule_min_score': h.rule_min_score_id.name if h.rule_min_score_id else None,
                    'attribute': h.subject_attributes_id.name if h.subject_attributes_id else None
                })

        return result

    def find_original_changed_rules_norule(self, area, period):
        period_str = str(period) if period != 0 else '000000'

        subject_rules = self.env['dara_mallas.subject_rule'].search([
            ('area_id.code', '=', area),
            ('period_id.name', '=', period_str)
        ])

        result = []

        for sr in subject_rules:
            homologation = sr.subject_homologation_ids 
            for h in homologation:
                result.append({
                    'period': period_str,
                    'area': sr.area_id.code,
                    'rule': sr.subject_id.code,
                    'condition': h.condition,
                    'conector': h.group_id.name,
                    'subject': h.homologation_subject_id.code,
                    'prueba': h.test if h.test != '0' else None,
                    'test puntaje minimo': h.min_score if h.test != '0' else None,
                    'test puntaje maximo': h.max_score if h.test != '0' else None,
                    'rule_min_score': h.rule_min_score_id.name if h.rule_min_score_id else None,
                    'attribute': h.subject_attributes_id.name if h.subject_attributes_id else None
                })

        return result

    def find_mirror_changed_rules(self, area, period, rule):
        period_str = str(period) if period != 0 else '000000'

        subject_rule_mirrors = self.env['dara_mallas.subject_rule_mirror'].search([
            ('area_id.code', '=', area),
            ('period_id.name', '=', period_str),
            ('subject_id.code', '=', rule)
        ])

        result = []

        for sr in subject_rule_mirrors:
            homologation_mirrors = sr.subject_homologation_ids  
            for h in homologation_mirrors:
                result.append({
                    'period': period_str,
                    'area': sr.area_id.code,
                    'rule': sr.subject_id.code,
                    'condition': h.condition,
                    'conector': h.group_id.name,
                    'subject': h.homologation_subject_id.code,
                    'prueba': h.test if h.test != '0' else None,
                    'test puntaje minimo': h.min_score if h.test != '0' else None,
                    'test puntaje maximo': h.max_score if h.test != '0' else None,
                    'rule_min_score': h.rule_min_score_id.name if h.rule_min_score_id else None,
                    'attribute': h.subject_attributes_id.name if h.subject_attributes_id else None
                })

        return result

    def find_current_areas_subject(self, area, period):
        # Search for the relevant area and period records
        area_homologations = self.env['dara_mallas.area_homologation'].search([
            ('area_id.code', '=', area),
            ('period_id.name', '=', period)
        ])

        result = []

        for ah in area_homologations:
            # Access the related subjects through subject_inherit_area
            for sia in ah.subject_inherit_area_ids:
                subject_code = sia.subject_inherit_id.subject_id.code
                if subject_code not in result:
                    result.append(subject_code)

        return result


    def generate_report(self):
        changed_rules = self.find_mirror_changed_rules_periods()
        if changed_rules:
            file_data = []
            for rule_period in changed_rules:
                # Obtenemos todas las reglas del área a la que corresponde la regla cambiada
                subject_homologations = self.find_original_changed_rules_norule(rule_period['area'], rule_period['period'])
                # Obtenemos las reglas actuales solo de la regla que cambió
                original_subject_homologations = self.find_original_changed_rules(str(rule_period['area']).strip(), str(rule_period['period']), str(rule_period['rule']))
                # Obtenemos las reglas anteriores de la espejo
                mirror_subject_homologations = self.find_mirror_changed_rules(str(rule_period['area']).strip(), str(rule_period['period']), str(rule_period['rule']))
                # Obtenemos las asignaturas actuales del área para validar posteriormente si se eliminó alguna de la malla
                current_subjects = self.find_current_areas_subject(rule_period['area'], rule_period['period'])
                for current_homologation in subject_homologations:
                    file_data.append([
                        current_homologation["period"],
                        current_homologation["area"],
                        current_homologation["rule"],
                        current_homologation["condition"],
                        current_homologation["conector"],
                        current_homologation["subject"],
                        current_homologation["prueba"],
                        current_homologation["test puntaje minimo"],
                        current_homologation["test puntaje maximo"],
                        current_homologation["rule_min_score"],
                        current_homologation["attribute"],
                    ])
                    for original_homologation in original_subject_homologations:
                        match_found = False
                        differences = []
                        for mirror_homologation in mirror_subject_homologations:
                            if original_homologation['rule'] == mirror_homologation['rule'] and original_homologation['subject'] == mirror_homologation['subject']:
                                match_found = True
                                for key in original_homologation:
                                    if original_homologation[key] != mirror_homologation[key]:
                                        differences.append((key, original_homologation[key], mirror_homologation[key]))
                                if differences and current_homologation["rule"] == original_homologation['rule']:
                                    file_data.append([
                                        original_homologation["period"],
                                        original_homologation["area"],
                                        original_homologation["rule"],
                                        original_homologation["condition"],
                                        original_homologation["conector"],
                                        original_homologation["subject"],
                                        original_homologation["prueba"],
                                        original_homologation["test puntaje minimo"],
                                        original_homologation["test puntaje maximo"],
                                        original_homologation["rule_min_score"],
                                        original_homologation["attribute"],
                                        'modified'
                                    ])
                                break

                        if not match_found and current_homologation["rule"] == original_homologation['rule'] and current_homologation["subject"] == original_homologation['subject']:
                            file_data.append([
                                original_homologation["period"],
                                original_homologation["area"],
                                original_homologation["rule"],
                                original_homologation["condition"],
                                original_homologation["conector"],
                                original_homologation["subject"],
                                original_homologation["prueba"],
                                original_homologation["test puntaje minimo"],
                                original_homologation["test puntaje maximo"],
                                original_homologation["rule_min_score"],
                                original_homologation["attribute"],
                                'add'
                            ])

                for mirror_homologation in mirror_subject_homologations:
                    match_found = False
                    for original_homologation in original_subject_homologations:
                        if original_homologation['rule'] == mirror_homologation['rule'] and original_homologation['subject'] == mirror_homologation['subject']:
                            match_found = True
                            break

                    if not match_found:
                        file_data.append([
                            mirror_homologation["period"],
                            mirror_homologation["area"],
                            mirror_homologation["rule"],
                            mirror_homologation["condition"],
                            mirror_homologation["conector"],
                            mirror_homologation["subject"],
                            mirror_homologation["prueba"],
                            mirror_homologation["test puntaje minimo"],
                            mirror_homologation["test puntaje maximo"],
                            mirror_homologation["rule_min_score"],
                            mirror_homologation["attribute"],
                            'remove'
                        ])
                                 
            seen = {}
            file_data_no_duplicates = []
            for row in file_data:
                row_tuple = tuple(row)
                if row_tuple not in seen:
                    seen[row_tuple] = True
                    file_data_no_duplicates.append(row)

            self.save_to_excel(file_data_no_duplicates)
         
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'dara_mallas.stop_sp_homologations',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
                'views': [(False, 'form')],
                'target': 'new',
                'name': 'Reporte de homologaciones malla congelada'
            }


    def save_to_excel(self, file_data):
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "Homologaciones Malla Congelada"

        fill_modified = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        fill_added = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")
        fill_removed = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")

        header = ["PERIODO", "AREA", "REGLA", "CONDICION", "CONECTOR", "SIGLA", "PRUEBA", "TEST PUNTAJE MINIMO", "TEST PUNTAJE MAXIMO", "REGLA PUNTAJE MINIMO", "ATRIBUTOS", "CAMBIOS"]
        ws1.append(header)

        for row in file_data:
            ws1.append(row)
            if row[-1] == "modified":
                for cell in ws1[ws1.max_row]:
                    cell.fill = fill_modified
            elif row[-1] == "add":
                for cell in ws1[ws1.max_row]:
                    cell.fill = fill_added
            elif row[-1] == "remove":
                for cell in ws1[ws1.max_row]:
                    cell.fill = fill_removed
            elif row[-1] == "regla removida del área":
                for cell in ws1[ws1.max_row]:
                    cell.fill = fill_removed

        output = BytesIO()
        wb.save(output)

        self.write({
            'file': base64.b64encode(output.getvalue()),
            'file_name': 'Homologaciones_Malla_Congelada_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.xlsx'
        })

        wb.close()
        output.close()


class curent_sp_homologations(models.Model):
    _name="dara_mallas.current_sp_homologations"
    file=fields.Binary("Reporte")
    file_name=fields.Char("Reporte de cambios en malla congelada")
    period_to_report = fields.Char("Periodo a reportar")