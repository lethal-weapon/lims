import csv

from django.http import HttpResponse


class ExportCsvMixin:

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class ImportCsvMixin:

    def import_as_csv(self, csv_file, model_form, encoding='utf-8'):
        lines = csv_file.read().decode(encoding).splitlines()
        all_data = self.process_csv(lines)

        for data in all_data:
            form = model_form(data)
            if form.is_valid():
                form.save()

    def process_csv(self, lines):
        # a list of dict, each dict stands for an object
        all_data = []

        # field_dict: (key, val) == (count, field name)
        field_dict, field_names = {}, lines[0].split(',')
        field_count = len(field_names)

        for field_name in field_names:
            field_count -= 1
            field_dict[field_count] = field_name

        # each line contains all field values of an object
        for line in lines[1:]:
            data_dict, data_fields = {}, line.split(',')
            data_count = len(data_fields)

            # data_dict: (key, val) == (count, field value)
            for field in data_fields:
                data_count -= 1
                data_dict[data_count] = field

            # data: (key, val) == (field name, field value)
            data = {}
            for count, name in field_dict.items():
                data[name] = data_dict[count]
            all_data.append(data)

        return all_data
