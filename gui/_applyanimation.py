from PySide6.QtCore import QPointF, QVariantAnimation, QTimeLine, QEasingCurve
from PySide6.QtWidgets import QGraphicsItemAnimation

class ApplyAnimation:
    def __init__(self, scene):
        self.scene = scene

    def applyAnimationsToPreview(self, layer) -> None:
        if not hasattr(layer, 'animations'):
            return

        for animation_element in layer.animations:
            targetId = layer.id
            keyPath = getattr(animation_element, "keyPath", None)
            if keyPath is None:
                continue
                
            for item in self.scene.items():
                if hasattr(item, "data") and item.data(0) == targetId:
                    anim = None
                    if animation_element.type == "CAKeyframeAnimation":
                        anim = self.applyKeyframeAnimationToItem(item, keyPath, animation_element)
                    elif animation_element.type == "CASpringAnimation":
                        anim = self.applySpringAnimationToItem(item, keyPath, animation_element)
                    
                    if anim:
                        self.animations.append(anim)

    def applyKeyframeAnimationToItem(self, item, keyPath, anim):
        if keyPath is None:
            return None
            
        animation = QVariantAnimation()
        animation.setTargetObject(item)
        animation.setPropertyName(keyPath.encode('utf-8'))
        
        duration = float(getattr(anim, "duration", 1.0))
        animation.setDuration(int(duration * 1000))

        if hasattr(anim, 'values') and hasattr(anim, 'keyTimes') and anim.values and anim.keyTimes:
            for i, val_obj in enumerate(anim.values):
                key_time = float(anim.keyTimes[i].value)
                animation.setKeyValueAt(key_time, val_obj.value)

        loop_count = float(getattr(anim, 'repeatCount', 1))
        animation.setLoopCount(int(loop_count) if loop_count > 0 else -1) # -1 for infinite

        return animation

    def applySpringAnimationToItem(self, item, keyPath, anim):
        # This needs a proper QPropertyAnimation with a QEasingCurve for spring,
        # or a custom physics-based implementation. For now, returning None.
        return None
        
    def applyTransitionAnimationToPreview(self, targetId, keyPath, animation) -> None:
        pass