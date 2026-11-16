"""Recria exclusivamente a base sintética; não acessa sistemas reais. Não altera o modelo embutido do PBIP."""
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
import random, csv, json
DASH=Path(__file__).resolve().parent
rng=random.Random(20261116)
ref=datetime(2026,11,16)
servicos={'Sistemas':['ERP','Portal interno','Relatórios','Integração'],
          'Infraestrutura':['Rede','Computadores','Impressoras','E-mail'],
          'Acessos':['Criar acesso','Redefinir senha','Permissões'],
          'Manutenção':['Elétrica','Climatização','Mobiliário']}
rows=[]
for n in range(1,1201):
    abertura=datetime(2026,1,1)+timedelta(days=rng.randrange(319),hours=rng.randrange(8,18),minutes=rng.randrange(60))
    area=rng.choices(list(servicos),weights=[32,36,22,10])[0]
    servico=rng.choice(servicos[area])
    dias=(ref-abertura).total_seconds()/86400
    fechado=rng.random() < (0.92 if dias>30 else 0.62)
    status='Fechado' if fechado else rng.choice(['Novo','Em atendimento','Pendente'])
    fechamento=min(abertura+timedelta(hours=rng.randint(2,180)),ref) if fechado else None
    duracao=round((fechamento-abertura).total_seconds()/86400,4) if fechado else None
    rows.append({'ID':n,'Data abertura':abertura.isoformat(' '),'Data fechamento':fechamento.isoformat(' ') if fechamento else '',
      'Status':status,'Área tratada':area,'Serviço':servico,
      'Atribuído - Grupo técnico':{'Sistemas':'Equipe Sistemas','Infraestrutura':'Equipe Suporte','Acessos':'Equipe Acessos','Manutenção':'Equipe Manutenção'}[area],
      'Mês abertura':abertura.strftime('%Y-%m'),'Tempo atendimento dias':duracao if duracao is not None else '',
      'Prioridade':rng.choice(['Baixa','Normal','Alta'])})
(DASH/'dados').mkdir(exist_ok=True)
with (DASH/'dados/chamados_sinteticos.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';'); w.writeheader(); w.writerows(rows)
contagens=Counter(r['Status'] for r in rows)
resumo={'total':len(rows),'status':dict(contagens),'tempo_medio_fechados_dias':round(sum(float(r['Tempo atendimento dias']) for r in rows if r['Status']=='Fechado')/contagens['Fechado'],4),
        'seed':20261116,'data_referencia':'2026-11-16','dados':'100% sintéticos'}
(DASH/'dados/resumo_validacao.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding='utf-8')

print("CSV sintético recriado. O modelo PBIP mantém a base já embutida.")
