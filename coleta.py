from playwright.sync_api import sync_playwright
import pandas as pd
import re
import time

BUSCAS = [
    "desenvolvedor mobile",
    "flutter",
    "android",
    "ios",
    "react native",
    "desenvolvedor software",
    "desenvolvedor backend",
    "desenvolvedor frontend",
    "programador python",
    "programador java",
    "programador c#",
    "engenheiro de software"
]

SITES_VAGAS = [
    "linkedin",
    "gupy",
    "indeed",
    "glassdoor",
    "catho",
    "revelo",
    "trampos",
    "infojobs",
    "vagas.com",
    "empregos.com",
    "jobgether",
    "jobleads",
    "jobilize",
    "bebee",
    "theirstack",
    "geekhunter",
    "remotar",
    "remotive",
    "wellfound",
    "workana",
    "upwork",
    "freelancer",
    "99freelas"
]

links = set()

with sync_playwright() as pw:

    browser = pw.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    for busca in BUSCAS:

        print(f"\nBuscando: {busca}")

        url = (
            "https://www.google.com/search?"
            f"q={busca.replace(' ', '+')}"
            "&ibp=htl;jobs"
            "&hl=pt-BR"
            "&gl=br"
        )

        page.goto(url)

        time.sleep(15)

        ultimo_total = 0
        sem_novos = 0

        while True:

            page.mouse.wheel(0, 5000)

            time.sleep(2)

            html = page.content()

            urls = set(
                re.findall(
                    r'https://[^\s"\']+',
                    html
                )
            )

            novos = 0

            for u in urls:

                if any(
                    site in u.lower()
                    for site in SITES_VAGAS
                ):
                    antes = len(links)
                    links.add(u)

                    if len(links) > antes:
                        novos += 1

            print(
                f"[{busca}] "
                f"novos={novos} "
                f"total={len(links)}"
            )

            if len(links) == ultimo_total:
                sem_novos += 1
            else:
                sem_novos = 0

            ultimo_total = len(links)

            if sem_novos >= 10:
                print("Fim da busca")
                break

    browser.close()

df = pd.DataFrame({
    "url": sorted(links)
})

df.to_excel(
    "vagas.xlsx",
    index=False
)

print(f"\nTotal salvo: {len(df)} vagas")