from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import *
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from datetime import datetime, timedelta


@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    if instance.status == "completed":

        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
        on_time_delivery_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = (
            on_time_delivery_pos.count() / completed_pos.count()
            if completed_pos.count() > 0
            else 0
        )

        HistoryPerfomence.objects.update_or_create(
            vendor=vendor, defaults={"on_time_delivery_rate": on_time_delivery_rate}
        )

    avg_quality = PurchaseOrder.objects.aggregate(Avg("quality_rating", default=0))
    print(avg_quality.get("quality_rating__avg"))

    # Calculate average response time
    average_response_time = (
        PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False, issue_date__isnull=False
        )
        .annotate(
            response_time=ExpressionWrapper(
                F("acknowledgment_date") - F("issue_date"), output_field=DurationField()
            )
        )
        .aggregate(avg_response_time=Avg("response_time"))["avg_response_time"]
    )
    if average_response_time:
        avg_response_seconds = (average_response_time).total_seconds()

    else:
        avg_response_seconds = None

    status_compleate_count = PurchaseOrder.objects.filter(status="completed").count()
    total_count = PurchaseOrder.objects.all().count()
    fulfillment_rate = status_compleate_count / total_count if total_count > 0 else 0
    HistoryPerfomence.objects.update_or_create(
        vendor=vendor,
        defaults={
            "quality_rating_avg": avg_quality["quality_rating__avg"],
            "quality_rating_avg": avg_quality["quality_rating__avg"],
            "average_response_time": average_response_time,
            "fulfillment_rate": fulfillment_rate,
        },
    )


@receiver(pre_save, sender=PurchaseOrder)
def update_object(sender, instance, **kwargs):
    try:
        vendor = instance.vendor

        old_instance = sender.objects.get(pk=instance.pk)
        if instance.status != old_instance.status and instance.status == "compleated":
            status_compleate_count = PurchaseOrder.objects.filter(
                status="completed"
            ).count()
            total_count = PurchaseOrder.objects.all().count()
            fulfillment_rate = (
                status_compleate_count / total_count if total_count > 0 else 0
            )
            HistoryPerfomence.objects.update_or_create(
                vendor=vendor, defaults={"fulfillment_rate": fulfillment_rate}
            )

    except sender.DoesNotExist:
        return {'msg':'DoesNotExist'}
