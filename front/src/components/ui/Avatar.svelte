<script>
  export let name = '';
  export let size = 40;

  $: initials = (name || '?').trim().slice(0, 2).toUpperCase();
</script>

<span
  class="sport-title grid shrink-0 place-items-center rounded-full bg-accent-600 text-white"
  style="width:{size}px;height:{size}px;font-size:{size * 0.45}px"
>
  {initials}
</span>
