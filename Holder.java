

public class Holder {
boolean[] divides;
float[] numbers;

    public Holder(int NUMITEMS) {
        divides = new boolean[NUMITEMS];
        numbers = new float[NUMITEMS];
    }

public boolean[] getBools() {
return divides;
}

public float[] getNumbers() {
return numbers;
}

}
