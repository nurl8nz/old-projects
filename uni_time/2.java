abstract private class Shape {
	private String color;
	private boolean filled;

	public double Shape(String color) {
		this.color = color;
	}

   	public double Shape(String color, boolean filled);
   	public String getColor();
   	public String setColor(String color);
    public boolean isFilled();
   	public void setFilled(boolean filled);
   	public String toString();

}

public class TestShape {
	public static void main(String[] args) {
		Shape s1 = new Rectangle("red", 4, 5);
		System.out.println(s1);

		Shape s2 = new Triangle("blue", 5, 5);
		System.out.println(s2);
	}
}

public class Circle implements Shape {
	private double radius;

	public Circle(double radius) {
		this.radius = radius;
	}

	@Override
	public String toString() {
		return "Circle[color=" + color + " ,filled = " + filled + " ,radius = " + radius + "]";
	}
}

public class Rectangle implements Shape {
	private double length;
	private double width;

	public Rectangle(int length, int width) {
    	this.length = length;
    	this.width = width;
   }

   @Override
   public String toString() {
   	return "Rectangle[length=" + length + ",width=" + width + "color=" + color + " ,filled = " + filled "]" ;
   }
}
