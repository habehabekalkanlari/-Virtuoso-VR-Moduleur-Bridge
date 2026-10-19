# Moduleur TouchOSC Controller

İlk kod denemem! 🎉

Shmøergh Moduleur analog modular synth sistemi için TouchOSC kontrol yüzeyi. Brain modülüne direkt bağlanarak MIDI2CV kontrolü sağlıyor.

> Bu proje [shmoergh/moduleur](https://github.com/shmoergh/moduleur) donanım projesi için bir yazılım kontrolcüsüdür.

![Moduleur Controller](https://img.shields.io/badge/TouchOSC-Compatible-brightgreen) ![MIDI](https://img.shields.io/badge/MIDI-Brain_Direct-blue) ![First Code](https://img.shields.io/badge/First%20Repo-%E2%9D%A4%EF%B8%8F-red)

## 🎛️ Özellikler

- **Moduleur panellerine sadık tasarım** - Siyah Eurorack stili
- **Brain modülüne direkt bağlantı** - WebMIDI ve TouchOSC MIDI
- **5 Modül:** VCO, VCF, ADSR+VCA, Mixer, Brain
- **MIDI2CV desteği** - Klavyeden Pitch CV (1V/oct) + Gate
- **Hide özelliği** - Panel header'ına tıklayınca küçülme (numpad modülünden port)

## 🚀 Demo

### Web (Localhost)

```bash
# 1. Repo'yu klonla
git clone https://github.com/KULLANICI_ADIN/moduleur-touchosc.git
cd moduleur-touchosc

# 2. Çalıştır
python server.py
# veya direkt
python -m http.server 8000

# 3. Tarayıcıda aç
http://localhost:8000
```

Dosyaya çift tıklayarak da çalışır - server gerekmez!

### TouchOSC

1. TouchOSC Editor'ü aç (hexler.net)
2. File > Open > `Moduleur_Brain_Controller.tosc`
3. Telefonuna Sync et
4. Brain modülünün MIDI input'una bağla

## 🔌 MIDI Mapping (Brain Firmware: brain-basic-midi2cv)

| Kontrol | MIDI CC | Açıklama |
|---------|---------|----------|
| VCO Coarse | CC 20 | Kaba akort |
| VCO Fine | CC 21 | İnce akort |
| VCF Cutoff | CC 74 | Filtre kesim frekansı |
| VCF Resonance | CC 71 | Rezonans |
| ADSR A/D/S/R | CC 73/75/76/72 | Zarf |
| Mixer CH1/CH2 | CC 7/8 | Kanal seviyesi |
| Brain Pot A/B/C | CC 16/17/18 | Brain potları |
| Klavye | Note On/Off | Pitch CV + Gate |

## 📁 Dosyalar

- `index.html` - Web controller (Web MIDI API)
- `Moduleur_Brain_Controller.tosc` - TouchOSC layout
- `Moduleur_Brain_Controller.xml` - XML kaynak
- `server.py` - Basit localhost server

## 🧠 Nasıl Çalışır?

Brain modülü (Raspberry Pi Pico) üzerinde `brain-basic-midi2cv` veya `le-controlleur` firmware'i çalışır. Bu controller:

1. Klavyeden gelen notayı MIDI Note On olarak gönderir
2. Brain bunu 1V/oct Pitch CV ve Gate sinyaline çevirir
3. Knoblar CC mesajları olarak Brain'in potlarını kontrol eder

## 🛠️ Geliştirme Hikayesi

Bu benim ilk GitHub repom! Başlangıçta basit bir TouchOSC numpad modülüydü (F-l-i-x/TouchOSC örneklerinden). Sonra Shmøergh Moduleur gibi profesyonel bir projeyi görünce seviye atlayıp tam bir modular synth controller'a dönüştürdüm.

- Numpad'den gelen: tag üzerinden label bağlantısı + hide özelliği
- Moduleur'den gelen: Gerçek analog modül layout'u + Brain entegrasyonu

## 📚 Kaynaklar

- [Moduleur Donanım](https://github.com/shmoergh/moduleur)
- [Brain SDK](https://github.com/shmoergh/brain-sdk)
- [TouchOSC](https://hexler.net/touchosc)
- [F-l-i-x TouchOSC Modules](https://github.com/F-l-i-x/TouchOSC)

## 📄 Lisans

MIT - İlk projem olduğu için açık kaynak!

## 🙏 Teşekkür

Shmøergh ekibine açık kaynak Moduleur için ve TouchOSC modül yapımcılarına ilham için teşekkürler.

---

**İlk commit, ilk repo! 🚀**
