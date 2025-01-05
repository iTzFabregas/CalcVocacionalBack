import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def generate_plot(valores, result_type, main=False):

    if result_type == 'parcial':
        labels = ["?", "?", "?", "?", "?", "?", "?" ,"?", "?"]
    else:
        labels = ["Computacao", "Eletrica", "Mecatronica", "Aeronautica", "Licenciatura", "Producao", "Materiais", "Civil", "Ambiental"]

    num_variaveis = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_variaveis, endpoint=False).tolist()
    valores_buf = valores + valores[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(12 , 8), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=11, fontweight=500) 
    ax.set_yticklabels([])

    ax.grid(color='#CCCCCC', linestyle='solid', linewidth=0.3)

    ax.spines['polar'].set_visible(False)
    # ax.spines['polar'].set_color('#555555')
    # ax.spines['polar'].set_linewidth(0.5)


    ax.plot(angles, valores_buf, linewidth=1.5, color='#04caca')
    ax.fill(angles, valores_buf, color='#06fdfd', alpha=0.3)

    if not main: 
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        return image_base64

    plt.savefig("grafico.png")


if __name__ == "__main__":
      valores = [16,9,21,7,-35,-3,-22,-44,-38]
      generate_plot(valores, 'total', True)