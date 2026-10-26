Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice("Microsoft Maria Desktop")
$synth.Rate = 2

$wavPath = "c:\Users\Vinicius\analise-eleicoes-2026\video\narracao.wav"
$synth.SetOutputToWaveFile($wavPath)

$text = "O que realmente aconteceu com os votos computados após as dezessete horas no segundo turno de ontem? " +
        "Segundo o Tribunal Superior Eleitoral, Lula foi reeleito com mais de sessenta e quatro milhões de votos contra cinquenta e nove milhões e oitocentos mil de Flávio Bolsonaro, com uma diferença de quatro milhões e quatrocentos e trinta mil votos. " +
        "Às dezesseis horas e trinta e dois minutos, o ministro Cristiano Zanin autorizou a votação até as dezenove horas apenas onde havia falta de transporte na Bahia e chuvas no Rio de Janeiro. " +
        "O total de votos registrados após as dezessete horas no Brasil inteiro foi de apenas trinta e quatro mil trezentos e trinta votos. " +
        "Isso representa zero vírgula zero três por cento dos votos e menos de um por cento da vantagem do vencedor. " +
        "Portanto, a virada às vinte horas decorreu da apuração normal do Nordeste, e o impacto dos votos após as dezessete horas no resultado da eleição é rigorosamente zero."

$synth.Speak($text)
$synth.Dispose()
Write-Output "Áudio gerado em: $wavPath"
