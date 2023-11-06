// Obtém o elemento do link de tela cheia
var fullscreenLink = document.getElementById('fullscreen-link');

// Verifica se o navegador suporta o modo de tela cheia
if (document.fullscreenEnabled || document.webkitFullscreenEnabled || document.mozFullScreenEnabled || document.msFullscreenEnabled) {
  // Adiciona o evento de clique ao link de tela cheia
  fullscreenLink.addEventListener('click', toggleFullScreen);
}

// Função para alternar o modo de tela cheia
function toggleFullScreen() {
  // Verifica se o documento está atualmente em modo de tela cheia
  if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
    // Sai do modo de tela cheia
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  } else {
    // Entra no modo de tela cheia
    var element = document.documentElement;
    if (element.requestFullscreen) {
      element.requestFullscreen();
    } else if (element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen();
    } else if (element.mozRequestFullScreen) {
      element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
      element.msRequestFullscreen();
    }
  }
}