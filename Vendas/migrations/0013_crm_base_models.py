from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Vendas', '0012_alter_estoque_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('empresa', models.CharField(blank=True, max_length=120, null=True)),
                ('cargo', models.CharField(blank=True, max_length=120, null=True)),
                ('valor_potencial', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('origem', models.CharField(choices=[('manual', 'Manual'), ('site', 'Site'), ('indicacao', 'Indicacao'), ('outro', 'Outro')], default='manual', max_length=20)),
                ('status', models.CharField(choices=[('novo', 'Novo'), ('qualificado', 'Qualificado'), ('desqualificado', 'Desqualificado'), ('convertido', 'Convertido')], default='novo', max_length=20)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads_responsavel', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pipeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EtapaPipeline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('ordem', models.PositiveIntegerField(default=0)),
                ('probabilidade', models.PositiveSmallIntegerField(default=0)),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='etapas', to='Vendas.pipeline')),
            ],
            options={
                'ordering': ['ordem', 'id'],
                'unique_together': {('pipeline', 'ordem')},
            },
        ),
        migrations.CreateModel(
            name='Oportunidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=140)),
                ('valor', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('status', models.CharField(choices=[('aberta', 'Aberta'), ('ganha', 'Ganha'), ('perdida', 'Perdida')], default='aberta', max_length=20)),
                ('previsao_fechamento', models.DateField(blank=True, null=True)),
                ('motivo_perda', models.TextField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('etapa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='oportunidades', to='Vendas.etapapipeline')),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oportunidades', to='Vendas.lead')),
                ('pipeline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='oportunidades', to='Vendas.pipeline')),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oportunidades_responsavel', to=settings.AUTH_USER_MODEL)),
                ('venda', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oportunidades', to='Vendas.venda')),
            ],
        ),
        migrations.CreateModel(
            name='InteracaoCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canal', models.CharField(choices=[('email', 'Email'), ('telefone', 'Telefone'), ('whatsapp', 'WhatsApp'), ('reuniao', 'Reuniao'), ('outro', 'Outro')], default='outro', max_length=20)),
                ('assunto', models.CharField(max_length=140)),
                ('mensagem', models.TextField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interacoes_cliente', to=settings.AUTH_USER_MODEL)),
                ('oportunidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interacoes', to='Vendas.oportunidade')),
            ],
        ),
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ligacao', 'Ligacao'), ('email', 'Email'), ('reuniao', 'Reuniao'), ('tarefa', 'Tarefa'), ('nota', 'Nota')], max_length=20)),
                ('titulo', models.CharField(max_length=140)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_prevista', models.DateTimeField(blank=True, null=True)),
                ('concluida', models.BooleanField(default=False)),
                ('data_conclusao', models.DateTimeField(blank=True, null=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('lead', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='atividades', to='Vendas.lead')),
                ('oportunidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='atividades', to='Vendas.oportunidade')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='atividades', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
