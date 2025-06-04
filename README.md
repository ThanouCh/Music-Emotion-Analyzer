# Music Emotion Analyzer

## Περιγραφή

Η εφαρμογή "Music Emotion Analyzer" αναλύει το συναίσθημα αγγλικών τραγουδιών από το YouTube. Δέχεται URL, εξάγει τον ήχο, μεταγράφει τους στίχους με το μοντέλο Whisper και αναλύει το συναίσθημα των στίχων χρησιμοποιώντας ένα προεκπαιδευμένο μοντέλο βαθιάς μάθησης. Τέλος, προτείνει σχετικά τραγούδια βασισμένα στο συναίσθημα.

## Απαιτήσεις

* Python 3.8+
* PyTorch
* Transformers (Hugging Face)
* faster-whisper
* yt-dlp
* pytube
* pydub
* gradio

## Εγκατάσταση

```bash
pip install yt-dlp faster-whisper transformers torch gradio pytube pydub
```

## Ροή Εργασίας

1. Ο χρήστης εισάγει το URL ενός τραγουδιού στο YouTube (αγγλικοί στίχοι).
2. Το βίντεο μετατρέπεται σε αρχείο .mp3 με `yt-dlp`.
3. Οι στίχοι εξάγονται με το μοντέλο `faster-whisper (medium)`.
4. Γίνεται ανάλυση συναισθήματος στους στίχους με το μοντέλο:

   * `bhadresh-savani/distilbert-base-uncased-emotion`
5. Προτείνονται σχετικά τραγούδια σύμφωνα με το ανιχνευμένο συναίσθημα.

## Υποστηριζόμενα Συναισθήματα

Το μοντέλο ταξινομεί σε έξι κατηγορίες:

* **anger** (θυμός)
* **fear** (φόβος)
* **joy** (χαρά)
* **love** (αγάπη)
* **sadness** (λύπη)
* **surprise** (έκπληξη)

## Παράδειγμα Χρήσης (Python)

```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
title, lyrics, emotion, suggestions = process_url(url)
print("Τίτλος:", title)
print("Στίχοι:", lyrics)
print("Συναίσθημα:", emotion)
```

## Web Interface (Gradio)

Η εφαρμογή διαθέτει γραφικό περιβάλλον χρήστη μέσω Gradio:

* Πληκτρολογήστε ένα YouTube URL
* Πατήστε Enter ή το κουμπί για ανάλυση
* Δείτε:

  * Τίτλο βίντεο
  * Στίχους
  * Συναίσθημα με ποσοστό βεβαιότητας
  * Προτεινόμενα τραγούδια

## Ιδιαίτερα Χαρακτηριστικά

* **Ολοκληρωμένη ανάλυση συναισθήματος** σε στίχους από YouTube.
* **Αυτόματη μετατροπή βίντεο σε ήχο και απομαγνητοφώνηση**.
* **Προτάσεις μουσικών κομματιών** σχετικών με το ανιχνευμένο συναίσθημα.
* **Βελτιστοποίηση χρήσης μνήμης GPU**, με καθαρισμό μεταξύ βημάτων.

## Περιορισμοί

* Το εργαλείο λειτουργεί μόνο με **αγγλικούς στίχους**.
* Ανάλυση συναισθήματος περιορίζεται στα πρώτα **512 tokens**.
* Το μοντέλο συναισθήματος είναι γενικό και δεν έχει εκπαιδευτεί ειδικά για μουσική.

## Μελλοντικές Βελτιώσεις

* Υποστήριξη πολλών γλωσσών (π.χ. Ελληνικά).
* Καλύτερη οπτικοποίηση των αποτελεσμάτων.
* Fine-tuning του μοντέλου σε dataset στίχων τραγουδιών.
* Υποστήριξη πολλών συναισθημάτων ανά τραγούδι.
* Δυναμική ανανέωση dictionary με προτάσεις από Spotify API ή YouTube API
* Άμεση σύνδεση με YouTube API για προτάσεις τραγουδιών βασισμένες στο συναίσθημα, καλλιτέχνη ή είδος μουσικής


## Πηγές / Αναφορές

* Whisper: [https://github.com/openai/whisper](https://github.com/openai/whisper)
* HuggingFace Emotion Model: [https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion)
* yt-dlp: [https://github.com/yt-dlp/yt-dlp](https://github.com/yt-dlp/yt-dlp)
* Gradio: [https://gradio.app/](https://gradio.app/)


