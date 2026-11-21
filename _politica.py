"""Genera la política de privacidad de una app de Crablion con suscripción (RevenueCat) y, si aplica, anuncios (AdMob).
uso:  python _politica.py <carpeta> "<Nombre de la app>" <package> <datos.html> [--anuncios]
  datos.html: el bloque <ul>…</ul> que describe qué datos maneja la app (sección 1).
Escribe <carpeta>/index.html y agrega la app a index.html.
"""
import sys
from pathlib import Path

R = Path(__file__).resolve().parent
carpeta, nombre, pkg, datos = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4]).read_text(encoding='utf-8')
anuncios = '--anuncios' in sys.argv
base = (R / 'gastos' / 'index.html').read_text(encoding='utf-8')
head = base[:base.index('<h1>')].replace('Control de gastos</title>', f'{nombre}</title>')

n = 1
def h(t):
    global n
    s = f'<h2>{n}. {t}</h2>'; n += 1; return s

partes = ['<h1>Política de privacidad</h1>',
          f'<p class="meta">{nombre} ({pkg}) · Crablion · Vigente desde el 21 de noviembre de 2026</p>',
          f'<p>Esta política explica qué información trata la app <strong>{nombre}</strong> (la “App”), publicada por Crablion en Google Play, y cómo se usa.</p>',
          h('Tus datos'), datos,
          h('Suscripción Pro (Google Play y RevenueCat)'),
          '<p>La App ofrece una versión Pro opcional (suscripción o pago único). El pago lo procesa <strong>Google Play</strong>; Crablion no recibe los datos de tu tarjeta. '
          'Para saber si tienes Pro, la App usa <strong>RevenueCat</strong> (RevenueCat, Inc.), que recibe un identificador anónimo generado por la App, el historial de compras de la App '
          '(producto, fecha, estado y token de compra) y datos técnicos básicos del dispositivo (modelo, versión de Android, idioma y país). Se usa solo para activar y validar tu compra, '
          'restaurarla y prevenir fraudes, y se transmite cifrado. Consulta la <a href="https://www.revenuecat.com/privacy" rel="noopener">Política de privacidad de RevenueCat</a>. '
          'Puedes cancelar la suscripción cuando quieras en Google Play → <em>Pagos y suscripciones</em>; si la cancelas, no se borra nada de lo que guardaste.</p>']
if anuncios:
    ads = base[base.index('<h2>2. Publicidad'):base.index('<h2>4. Datos que no')]
    ads = ads.replace('<h2>2. Publicidad', h('Publicidad') .replace('</h2>', '') , 1).replace('<h2>3. Tus opciones', h('Tus opciones').replace('</h2>', ''), 1)
    ads = ads.replace('La App es gratuita y muestra anuncios', 'La versión gratuita de la App muestra anuncios').replace('mediante Google AdMob', 'mediante Google AdMob (la versión Pro no muestra anuncios)')
    partes.append(ads)
else:
    partes += [h('Publicidad'), '<p>La App <strong>no muestra anuncios</strong> y no usa el ID de publicidad.</p>']
partes += [h('Datos que no recopilamos'), '<p>La App no requiere cuenta ni inicio de sesión. Crablion no recopila tu nombre, correo, contactos, ubicación ni el contenido que guardas en la App.</p>',
           h('Menores de edad'), '<p>La App no está dirigida a menores de 13 años y no recopila a sabiendas información personal de niños.</p>',
           h('Cambios a esta política'), '<p>Si esta política cambia, publicaremos la nueva versión en esta misma página con su fecha de vigencia.</p>',
           h('Contacto'), '<p>Si tienes preguntas sobre esta política o sobre tus datos, escríbenos a <a href="mailto:crablion99@gmail.com">crablion99@gmail.com</a>.</p>',
           '</main>\n</body>\n</html>\n']
(R / carpeta).mkdir(exist_ok=True)
(R / carpeta / 'index.html').write_text(head + '\n\n'.join(partes), encoding='utf-8')
idx = (R / 'index.html').read_text(encoding='utf-8')
if f'href="{carpeta}/"' not in idx:
    idx = idx.replace('  <li><a href="inventario/">', f'  <li><a href="{carpeta}/">{nombre}</a></li>\n  <li><a href="inventario/">')
    (R / 'index.html').write_text(idx, encoding='utf-8')
print('ok', carpeta, '(con anuncios)' if anuncios else '(sin anuncios)')
