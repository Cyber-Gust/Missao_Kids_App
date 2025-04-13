# src/utils/helpers.py

from PyQt5.QtCore import QSize, QPoint

class WindowStateManager:
    """Classe para gerenciar o estado da janela entre as telas"""
    
    _instance = None
    _size = None
    _position = None
    _is_maximized = False
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = WindowStateManager()
        return cls._instance
    
    def save_state(self, window):
        """Salva o estado atual da janela"""
        self._is_maximized = window.isMaximized()
        if not self._is_maximized:
            self._size = window.size()
            self._position = window.pos()
    
    def restore_state(self, window):
        """Restaura o estado salvo para a janela"""
        if self._is_maximized:
            window.showMaximized()
        elif self._size is not None:
            window.resize(self._size)
            if self._position is not None:
                window.move(self._position)