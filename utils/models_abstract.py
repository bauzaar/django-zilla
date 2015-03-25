# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.html import escape
from django.db.models import Model, DateTimeField, PositiveIntegerField, SlugField, TextField, \
    CharField, BooleanField, DecimalField
from baubackend.apps.utils.datetime_utils import get_utc_now


class SEOModel(Model):
    meta_title = CharField(max_length=200, blank=True)
    meta_description = TextField(blank=True)
    meta_keywords = TextField(blank=True)

    class Meta:
        abstract = True


class SluggableModel(Model):
    slug = SlugField(max_length=200, verbose_name='URL slug', unique=True, db_index=True)

    class Meta:
        abstract = True


class SluggableBlankModel(Model):
    slug = SlugField(max_length=200, verbose_name='URL slug', unique=True, db_index=True, blank=True)

    class Meta:
        abstract = True


class LinkableFieldModel(Model):
    def get_change_url(self):
        try:
            return reverse(
                "admin:%s_%s_change" % (self._meta.app_label, self._meta.object_name.lower()), args=(self.pk,))
        except Exception as e:
            return unicode(e)

    def get_change_href(self):
        return '<strong><a href="%s">%s</a></strong>' % (self.get_change_url(), escape(self))
    get_change_href.allow_tags = True
    get_change_href.short_description = 'Link'

    class Meta:
        abstract = True


class TimedatedModel(Model):
    timestamp_creazione = DateTimeField(default=get_utc_now, auto_now_add=True, db_index=True, editable=False)
    timestamp_modifica = DateTimeField(default=get_utc_now, auto_now=True, verbose_name="Ultima modifica",
                                       db_index=True, editable=False)

    class Meta:
        abstract = True


class PreviewImageModel(Model):
    def get_immagine(self):
        return self.immagine

    def tag_immagine(self):
        w, h = self.get_image_thumbnail_size()
        return '<img src="%s" width=%spx height=%spx />' % (self.get_immagine().url, w, h)
    tag_immagine.short_description = 'Anteprima'
    tag_immagine.allow_tags = True

    def get_image_thumbnail_size(self):
        max_dim = settings.THUMBNAIL_MAX_DIM
        ratio = max_dim / max(self.get_immagine().width, self.get_immagine().height)
        return int(self.get_immagine().width * ratio), int(self.get_immagine().height * ratio)

    class Meta:
        abstract = True


class PositionableModel(Model):
    posizione = PositiveIntegerField()

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.posizione is None:
            try:
                last = model.objects.order_by('-posizione')[0]
                self.posizione = last.posizione + 1
            except IndexError:
                self.posizione = 0 # First row
        return super(PositionableModel, self).save(*args, **kwargs)

    class Meta:
        ordering = ('posizione',)
        abstract = True


class LockedModel(Model):
    locked = BooleanField(default=False)

    def lock(self):
        self.locked = True
        super(LockedModel, self).save()

    def unlock(self):
        self.locked = False
        super(LockedModel, self).save()

    class Meta:
        abstract = True


class PropagateSellableMixin(object):
    def handle_sellable(self):
        from baubackend.apps.erp.models import Referenza, PaginaVendita
        super(PropagateSellableMixin, self).save()

        qs_referenze_Locked = Referenza.objects.select_for_update().filter(
            id__in=self.paginavendita_referenza_set.values_list('referenza'))
        qs_pagina_vendita_Locked = PaginaVendita.objects.select_for_update().filter(
            id__in=self.paginavendita_referenza_set.values_list('pagina_vendita'))

        for paginavendita_referenza in self.paginavendita_referenza_set.select_for_update():
            b = not paginavendita_referenza.dismessa \
                and paginavendita_referenza.pagina_vendita.online \
                and paginavendita_referenza.referenza.online
            paginavendita_referenza.sellable = b
            paginavendita_referenza.save()

        for referenza_Locked in qs_referenze_Locked:
            referenza_Locked.sellable = referenza_Locked.paginavendita_referenza_set.filter(
                sellable=True).exists()
            super(PropagateSellableMixin, referenza_Locked).save()

        for pagina_vendita_Locked in qs_pagina_vendita_Locked:
            pagina_vendita_Locked.sellable = pagina_vendita_Locked.paginavendita_referenza_set.filter(
                sellable=True).exists()
            super(PropagateSellableMixin, pagina_vendita_Locked).save()

        from baubackend.apps.cart.models import RigaCarrello
        for riga_carrello in RigaCarrello.objects.filter(
                carrello__ordine__isnull=True, paginavendita_referenza__sellable=False):
            riga_carrello.delete()


class ShippingFeesModel(Model):
    consegna_al_piano = BooleanField(default=False)
    spese_gestione = DecimalField(max_digits=4, decimal_places=2, verbose_name='Gestione ordine e imballo',
                                  default=settings.SPESE_GESTIONE)

    def get_descrizione_spese(self):
        contrassegno = hasattr(self, 'contrassegno') and self.contrassegno or False

        if self.consegna_al_piano and contrassegno:
            return 'al piano e contrassegno'
        if self.consegna_al_piano:
            return 'al piano'
        if contrassegno:
            return 'contrassegno'

    class Meta:
        abstract = True


class GoogleShoppingSkipModel(Model):
    skip_google_shopping = BooleanField(default=False)

    class Meta:
        abstract = True