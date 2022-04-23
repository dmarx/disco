export class Elements{

  public static setButtonAvailability(element, available) {
    element.classList[available ? 'add' : 'remove'](['active', 'btn-kl']);
    element.disabled = !available;
  }

}